import os
import sys
from dockerfile_parse import DockerfileParser
import requests
import json

if 'DRONE_PULL_REQUEST' not in os.environ:
    os.environ['DRONE_PULL_REQUEST'] = None

msg = {
    'build':{
        'author': os.environ['DRONE_COMMIT_AUTHOR'],
        'created': os.environ['DRONE_BUILD_CREATED'],
        'message': os.environ['DRONE_COMMIT_MESSAGE'],
        'number': os.environ['DRONE_BUILD_NUMBER'],
        'commit': os.environ['DRONE_COMMIT_SHA'],
        'branch': os.environ['DRONE_COMMIT_BRANCH'],
        'job': os.environ['DRONE_JOB_NUMBER'],
        'pull_request': os.environ['DRONE_PULL_REQUEST']
    },
    'repo':{
        'owner': os.environ['DRONE_REPO_OWNER'],
        'name': os.environ['DRONE_REPO_NAME']
    },
    'container': {}
}

if os.environ['DRONE_PULL_REQUEST']:
    print("WARN: this is a pull request %s" % (str(os.environ['DRONE_PULL_REQUEST'])))


content = None
with open(sys.argv[1], 'r') as content_file:
        content = content_file.read()

dfp = DockerfileParser()
dfp.content = content

msg['container']['labels'] = dfp.labels
print('Send: '+str(msg))
r = requests.post(os.environ['BIOCONTAINERS_URL'], json = msg)
if r.status_code != 200:
    print(r.text)
    sys.exit(1)
