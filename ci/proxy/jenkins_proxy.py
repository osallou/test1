from flask import Flask
from flask import request
import json
import copy
import logging
import os

import arrow
import requests

app = Flask(__name__)

jenkins_url = 'http://localhost:8080/job/'
if 'JENKINS_URL' in os.environ:
    jenkins_url = os.environ['JENKINS_URL']

@app.route('/hook', methods=['POST'])
def payload():
        # print(request.content_type)
        # print(str(request.form))
        # logging.error(request.form)
        try:
            payload = json.loads(request.form.get('payload'))
            commits = []
            if 'commits' in payload:
                commits = payload['commits']
            elif 'pull_request' in payload:
                res = requests.get(
                    payload['pull_request']['url'] + '/files',
                    headers={'Accept': 'application/vnd.github.v3+json'}
                )
                files = res.json()
                containers = []
                for pull_file in files:
                    container_path = '/'.join(pull_file['filename'].split('/')[:-1])
                    if container_path not in containers:
                        containers.append(container_path)
                if len(containers) > 1 or len(containers) == 0:
                    logging.error("ko, can't modify multiple containers in a same pull request")
                    return "ko, can't modify multiple containers in a same pull request"
                container_dir = containers[0].split('/')
                r = requests.get(jenkins_url + 'container-testci-pr/buildWithParameters?FORCE_CONTAINER='+container_dir[0]+'&FORCE_TOOL_VERSION='+container_dir[1]+'&PULL_REQUEST_ID='+payload['number'])
                return "ok"

            new_commits = {}
            for commit in commits:
                modified_container = []
                modified_commits = []
                updated = False
                if 'added' not in commit:
                    commit['added'] = []
                for modified in commit['added']:
                    container_path = '/'.join(modified.split('/')[:-1])
                    if container_path and container_path not in modified_container:
                        modified_container.append(container_path + '/Dockerfile')
                        updated = True
                if 'modified' not in commit:
                    commit['modified'] = []
                for modified in commit['modified']:
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
            if not new_commits and 'GITHUB_STATUS_TOKEN' in os.environ:
                    headers = {
                        'Accept': 'application/vnd.github.v3+json',
                        'Authorization': 'token ' + str(os.environ['GITHUB_STATUS_TOKEN'])
                    }
                    if 'pull_request' in payload:
                        github_url = payload['pull_request']['url'] + '/comments'
                    else:
                        github_url = payload['head_commit']['url'] + '/comments'

                    res = requests.post(
                        github_url,
                        json={
                            'body': 'no file modified, skipping request',
                        },
                        headers=headers
                    )
                    logging.warn('No commit to dispatch')

            for d in new_commits:
                logging.debug('headers: '+str(request.headers))
                logging.debug('data: '+json.dumps(new_commits[d]['payload']))
                container_dir = d.split('/')
                loggin.debug('Call:' + jenkins_url + 'container-testci/buildWithParameters?FORCE_CONTAINER='+container_dir[0]+'&FORCE_TOOL_VERSION='+container_dir[1]+'&FORCE_SHA1='+new_commits[d]['payload']['head_commit'])
                r = requests.get(jenkins_url + 'container-testci/buildWithParameters?FORCE_CONTAINER='+container_dir[0]+'&FORCE_TOOL_VERSION='+container_dir[1]+'&FORCE_SHA1='+new_commits[d]['payload']['head_commit'])
                logging.debug('post result '+str(r.status_code))
                logging.debug(str(r.text))
                # print(json.dumps(new_commits[d]['payload']))
        except Exception as e:
            logging.exception(str(e))
        return "ok"


if __name__ == '__main__':
          app.run(host='0.0.0.0')