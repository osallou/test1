import os
import sys
from dockerfile_parse import DockerfileParser
import requests
import json

msg = {
    'build':{
        'author': os.environ['DRONE_COMMIT_AUTHOR'],
        'created': os.environ['DRONE_BUILD_CREATED'],
        'message': os.environ['DRONE_COMMIT_MESSAGE'],
        'number': os.environ['DRONE_BUILD_NUMBER'],
        'commit': os.environ['DRONE_COMMIT_SHA']
    },
    'repo':{
        'owner': os.environ['DRONE_REPO_OWNER'],
        'name': os.environ['DRONE_REPO_NAME']
    },
    'container': {}
}


content = None
with open(sys.argv[1], 'r') as content_file:
        content = content_file.read()

dfp = DockerfileParser()
dfp.content = content

msg['container']['labels'] = dfp.labels

r = requests.post(os.environ['BIOCONTAINERS_URL'], json = msg)
if r.status_code == 200:
    print(r.text)
    sys.exit(1)
