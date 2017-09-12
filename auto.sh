#!/bin/bash

set -e

echo "Check modified files"
git show --name-status $DRONE_COMMIT_SHA | grep '^[MA]\s'  | sed -e 's/^[MA]\s*//g' | while read i; do echo $i ; done > /tmp/out
while read p
do
    echo "Check $p"
    curfile=`basename $p`
    if [ $curfile == "Dockerfile" ]
    then
        echo "PLUGIN_DOCKERFILE=$p" > DRONE_ENV
        major=`sed -n 's/.*\ssoftware.version="\(.*\)"/\1/p' $p`
        minor=`sed -n 's/.*\sversion="\(.*\)"/\1/p' $p`
        version=$major-$minor
        if [ "$minor" == "" ]
        then
            version=$major
        fi
        software=`sed -n 's/.*\ssoftware="\(.*\)"/\1/p' $p`
        if [ $version == "-" ]
        then
            echo "Could not extract version from Dockerfile: $p"
            exit 1
        fi
        echo "PLUGIN_TAG=$version" >> DRONE_ENV
        echo "PLUGIN_REPO=osallou/$software" >> DRONE_ENV
    fi

done < /tmp/out
rm -f /tmp/out
cat DRONE_ENV
