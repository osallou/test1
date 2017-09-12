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
        major=`sed -n 's/LABEL\s*software.version="\(.*\)"/\1/p' $p`
        minor=`sed -n 's/LABEL\s*version="\(.*\)"/\1/p' $p`
        version=$major-$minor
        echo "PLUGIN_TAG=$version" >> DRONE_ENV
    fi

done < /tmp/out
rm -f /tmp/out
cat DRONE_ENV
