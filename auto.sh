#!/bin/bash

git show --name-status $DRONE_COMMIT_SHA | grep '^[MAD]\s'  | sed -e 's/^[MAD]\s*//g' | while read i; do dirname $i ; done > /tmp/out
while read p
do
    curfile=`basename $p`
    if [ $curfile == "Dockerfile" ]
    then
        echo "PLUGIN_DOCKERFILE=$p" > DRONE_ENV
        major=`sed -n 's/LABEL\s*software.version="\(.*\)"/\1/p' test.txt`
        minor=`sed -n 's/LABEL\s*version="\(.*\)"/\1/p' test.txt`
        version=$major-$minor
        echo "PLUGIN_TAG=$version" >> DRONE_ENV
    fi

done < /tmp/out
rm -f /tmp/out
cat DRONE_ENV
