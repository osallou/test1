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
        container=`sed -n 's/.*\scontainer="\(.*\)"\s*\\\*/\1/p' $p`
        if [ "$container" == "" ]
        then
            echo "no container name, use software name"
        else
            software=$container
        fi
        if [ "$version" == "-" ]
        then
            echo "Could not extract version from Dockerfile: $p"
            exit 1
        fi
        if [ "$DRONE_BUILD_EVENT" == "pull_request" ] || [ "$DRONE_BRANCH" != "master"]
        then
            version = "dev-$version"
            # Here could use local registry
            echo "PLUGIN_REPO=openstack-192-168-100-43.genouest.org/osallou/$software" >> DRONE_ENV
        else
            # Here could send to dockerhub
            echo "PLUGIN_REPO=openstack-192-168-100-43.genouest.org/osallou/$software" >> DRONE_ENV
        fi
        echo "DOCKERFILE=$p" >> DRONE_ENV
        echo "PLUGIN_TAG=$version" >> DRONE_ENV
        echo "BIOCONTAINER_DIR=$dirfile" >> DRONE_ENV
        echo "PLUGIN_REGISTRY=openstack-192-168-100-43.genouest.org" >> DRONE_ENV
        if [ "$DRONE_BUILD_EVENT" == "pull_request" ]
        then
            echo -e "\033[0;31mWARN:\033[0 this is a pull request, skip push of image"
            echo "PLUGIN_DRY_RUN=1" >> DRONE_ENV
        fi
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
