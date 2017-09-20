#!/bin/bash

set -e

echo "Check modified files"
git show --name-status $DRONE_COMMIT_SHA | grep '^[MA]\s'  | sed -e 's/^[MA]\s*//g' | while read i; do echo $i ; done > /tmp/out
cat /tmp/out
IS_DOCKER_FILE=0
while read p
do
    echo "Check $p"
    curfile=`basename $p`
    dirfile=`dirname $p`
    if [ $curfile == "Dockerfile" ]
    then
        IS_DOCKER_FILE=1
        echo "PLUGIN_DOCKERFILE=$p" > DRONE_ENV
        major=`sed -n 's/.*\ssoftware.version="\(.*\)"\s*\\\*/\1/p' $p`
        minor=`sed -n 's/.*\sversion="\(.*\)"\s*\\\*/\1/p' $p`
        version=$major-$minor
        echo "## $version ==> $minor"
        if [ "$minor" == "" ]
        then
            version=$major
        fi
        software=`sed -n 's/.*\ssoftware="\(.*\)"\s*\\\*/\1/p' $p`
        if [ "$version" == "-" ]
        then
            echo "Could not extract version from Dockerfile: $p"
            exit 1
        fi
        echo "PLUGIN_TAG=$version" >> DRONE_ENV
        echo "PLUGIN_REPO=openstack-192-168-100-43.genouest.org/osallou/$software" >> DRONE_ENV
        echo "BIOCONTAINER_DIR=$dirfile" >> DRONE_ENV
        echo "PLUGIN_REGISTRY=openstack-192-168-100-43.genouest.org"
    else
        echo "No Dockerfile here, skipping"
    fi

done < /tmp/out

if [ $IS_DOCKER_FILE == 0 ]
then
    echo "No Dockerfile found"
    exit 1
fi

rm -f /tmp/out
cat DRONE_ENV
