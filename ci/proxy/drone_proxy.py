from flask import Flask
from flask import request
import json
import copy
import logging
import os

import arrow
import requests

app = Flask(__name__)

drone_url = 'http://localhost:8000'
if 'DRONE_URL' in os.environ:
    drone_url = os.environ['DRONE_URL']

@app.route('/ping', methods=['GET'])
def ping():
    return "pong"

@app.route('/hook', methods=['POST'])
def payload():
        # print(request.content_type)
        # print(str(request.form))
        try:
            payload = json.loads(request.form.get('payload'))
            commits = payload['commits']
            drone_modified = False
            new_commits = {}
            for commit in commits:
                modified_container = []
                modified_commits = []
                updated = False
                for modified in commit['added']:
                    if modified.startswith('ci'):
                        continue
                    if modified.startswith('.drone.yml'):
                        drone_modified = True
                    container_path = '/'.join(modified.split('/')[:-1])
                    if container_path and container_path not in modified_container:
                        modified_container.append(container_path + '/Dockerfile')
                        updated = True
                for modified in commit['modified']:
                    if modified.startswith('ci'):
                        continue
                    if modified.startswith('.drone.yml'):
                        drone_modified = True
                    container_path = '/'.join(modified.split('/')[:-1])
                    if container_path and container_path not in modified_container:
                        modified_container.append(container_path + '/Dockerfile')
                        updated = True
                if updated:
                    modified_commits.append(commit['id'])
                for modif in modified_container:
                    commit['added'] = []
                    commit['modified'] = [modif]
                    commit['removed'] = []
                    container_dir = '/'.join(modif.split('/')[:-1])
                    commit['message'] = container_dir + ':' + commit['message']
                    commit_dict = copy.deepcopy(payload)
                    commit_dict['commits'] = [commit]
                    commit_dict['head_commit'] = commit
                    commit_dict['added'] = []
                    commit_dict['removed'] = []
                    commit_dict['modified'] = [modif]
                    if container_dir not in new_commits:
                        new_commits[container_dir] = {'date': arrow.get(commit['timestamp']).datetime, 'payload': commit_dict}
                    else:
                        if new_commits[container_dir]['date'] > arrow.get(commit['timestamp']).datetime:
                            new_commits[container_dir] = {'date': arrow.get(commit['timestamp']).datetime, 'payload': commit_dict}
            event = request.headers['X-GitHub-Event']
            if drone_modified and event == 'pull_request':
                logging.error('tried to modified .drone.yml in a pull request, forbidden:' + json.dumps(payload))
                return "ko"
            for d in new_commits:
                logging.debug('headers: '+str(request.headers))
                logging.debug('data: '+json.dumps(new_commits[d]['payload']))
                r = requests.post(drone_url + '/hook?access_token='+request.form.get('access_token'), data={'payload': json.dumps(new_commits[d]['payload'])}, headers=request.headers)
                logging.debug('post result '+str(r.status_code))
                logging.debug(str(r.text))
                # print(json.dumps(new_commits[d]['payload']))
        except Exception as e:
            logging.exception(str(e))
        return "ok"


if __name__ == '__main__':
          app.run(host='0.0.0.0')
