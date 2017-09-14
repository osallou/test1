#!/bin/sh

/usr/local/bin/dockerd --data-root /var/lib/docker
sleep 10
. ./DRONE_ENV
/usr/local/bin/docker run --rm $1 echo hello $PLUGIN_TAG
