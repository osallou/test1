from dockerfile_parse import DockerfileParser
import requests
import sys
import os
import logging
import re

def send_status(software, status, msg=None):
    repo = os.environ['DRONE_REPO']
    commit = os.environ['DRONE_COMMIT_SHA']
    info = 'Checking recipe metadata'
    if msg:
        info = ', '.join(msg)
    is_success = 'success'
    if status is None:
        is_success = 'pending'
    if status is False:
        is_success = 'failure'
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token ' + str(os.environ['GITHUB_STATUS_TOKEN'])
    }
    try:
        github_url = 'https://api.github.com/repos/%s/statuses/%s' % (repo, commit)
        res = requests.post(
            github_url,
            json={
                'description': info,
                'state': is_success,
                'context': 'biocontainers/status/check/' + str(software)
            },
            headers=headers
        )
        logging.warn('Send status info at %s: %s' % (github_url, str(res.status_code)))
    except Exception as e:
        logging.exception(str(e))

docker_file = None
if len(sys.argv) > 1 and sys.argv[1]:
    docker_file = sys.argv[1]

if not docker_file or not os.path.exists(docker_file):
    send_status(False, 'could not find any Dockerfile')
    sys.exit(1)

with open(docker_file, 'r') as content_file:
        content = content_file.read()

dfp = DockerfileParser()
dfp.content = content
labels = dfp.labels
status = True
msg = []
if 'software' not in labels or not labels['software']:
    status = False
    msg.append('software label not present')

software = labels['software']

pattern=re.compile("^([a-zA-Z0-9_-])+$")
if pattern.match(software) is None:
    logging.error(software + " has invalid name" )
    if 'container' in labels:
        if pattern.match(labels['container']) is None:
            status = False
            msg.append('software name is invalid for a container, it does not match expected regexp [a-zA-Z0-9_-], please use the *container* label to specify a software name compatible with container naming rules.')


if 'software.version' not in labels or not labels['software.version']:
    status = False
    msg.append('software.version label not present')

if 'description' not in labels or not labels['description'] or len(labels['description']) < 20:
    status = False
    msg.append('description label not present or too short')

if 'website' not in labels or not labels['website']:
    status = False
    msg.append('website label not present')

if 'license' not in labels or not labels['license']:
    status = False
    msg.append('license label not present')

version = labels['software.version']
if 'version' in labels and labels['version']:
    version = version + '-' + labels['version']

is_pull_or_dev = False
if os.environ['DRONE_BUILD_EVENT'] == 'pull_request' or os.environ['DRONE_BRANCH'] != 'master':
    is_pull_or_dev = True
    version = 'dev-' + version

with open('DRONE_ENV', 'a') as content_file:
    content_file.write('\nPLUGIN_TAG=' + version + '\n')
    content_file.write('SOFTWARE_NAME=' + labels['software'] + '\n')

send_status(software, status, msg)

with open('DRONE_ENV', 'r') as content_file:
    content = content_file.read()
    logging.warn(content)

if not status:
    sys.exit(1)
