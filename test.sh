#!/bin/sh
set -e
. ./DRONE_ENV
echo "check for ./$BIOCONTAINER_DIR/test.sh"
if [ -e ./$BIOCONTAINER_DIR/test.sh ]; then
    /usr/local/bin/dockerd --data-root /var/lib/docker --dns 192.168.100.43&
    echo "Wait for docker daemon"
    sleep 10
    echo "Creds:  "$${DOCKER_USERNAME} $${DOCKER_PASSWORD}
    /usr/local/bin/docker login -u $${DOCKER_USERNAME} -p $${DOCKER_PASSWORD} $PLUGIN_REGISTRY
    /usr/local/bin/docker run -v ${PWD}/$BIOCONTAINER_DIR:/mnt/biocontainers --rm $PLUGIN_REPO:$PLUGIN_TAG /mnt/biocontainers/test.sh
else
    echo "No test script available"
fi
