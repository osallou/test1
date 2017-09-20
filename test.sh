#!/bin/sh
set -e
. ./DRONE_ENV
echo "check for ./$BIOCONTAINER_DIR/test.sh"
if [ -e ./$BIOCONTAINER_DIR/test.sh ]; then
    /usr/local/bin/dockerd --data-root /var/lib/docker --dns 192.168.100.43&
    echo "Wait for docker daemon"
    sleep 10
    echo "Creds:  "${TEST_USERNAME} ${TEST_PASSWORD}
    /usr/local/bin/docker login -u ${TEST_USERNAME} -p ${TEST_PASSWORD} $PLUGIN_REGISTRY
    /usr/local/bin/docker run -v ${PWD}/$BIOCONTAINER_DIR:/mnt/biocontainers --rm $PLUGIN_REPO:$PLUGIN_TAG /mnt/biocontainers/test.sh
else
    echo "No test script available"
fi
