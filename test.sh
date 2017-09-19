#!/bin/sh
set -e
. ./DRONE_ENV
echo "check for ./$BIOCONTAINER_DIR/test.sh"
if [ -e ./$BIOCONTAINER_DIR/test.sh ]; then
    /usr/local/bin/dockerd --data-root /var/lib/docker &
    echo "Wait for docker daemon"
    sleep 10
    /usr/local/bin/docker run -v ${PWD}/$BIOCONTAINER_DIR:/mnt/biocontainers --rm $PLUGIN_REPO:$PLUGIN_TAG /mnt/biocontainers/test.sh
else
    echo "No test script available"
fi
