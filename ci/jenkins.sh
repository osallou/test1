#!/bin/bash

set -e

echo "Check modified files"
git show --name-status $GIT_COMMIT | grep '^[MA]\s'  | sed -e 's/^[MA]\s*//g' | while read i; do echo $i ; done > /tmp/out
cat /tmp/out
IS_DOCKER_FILE=0
while read p
do
    echo "Check $p"
    curfile=`basename $p`
    arrIN=(${curfile//\// })
    containerDir=${arrIN[0]}
    containerVersion=${arrIN[1]}
    dockerFile=$containerDir/$containerVersion/Dockerfile
    echo "Check docker file exists: $dockerFile"
    if [ -e $dockerFile ];
    then
        IS_DOCKER_FILE=1
    fi
    software=`sed -n 's/.*\ssoftware="\(.*\)"\s*\\\*/\1/p' $p | tr -d '[:space:]'`
    container=`sed -n 's/.*\scontainer="\(.*\)"\s*\\\*/\1/p' $p | tr -d '[:space:]'`
    if [ "$container" == "" ]
    then
        echo "no container name, use software name"
    else
        software=$container
    fi
    echo "DOCKERFILE=$p" > BIOCONTAINERS_ENV
    echo "CONTAINER=$software" >> BIOCONTAINERS_ENV
    echo "TOOL_VERSION=$containerVersion" >> BIOCONTAINERS_ENV
done < /tmp/out

if [ $IS_DOCKER_FILE == 0 ]
then
    echo "No Dockerfile found"
    exit 1
fi

rm -f /tmp/out
cat BIOCONTAINERS_ENV
