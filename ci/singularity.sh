#!/bin/bash

. ./DRONE_ENV

apt-get update && \
    apt-get install -y \
    python \
    dh-autoreconf \
    build-essential \
    squashfs-tools \
    git


git clone https://github.com/singularityware/singularity.git
cd singularity && ./autogen.sh && ./configure --prefix=/usr/local --sysconfdir=/etc && make && make install

echo "Bootstrap: docker" > singularity
echo "From: $PLUGIN_REPO:$PLUGIN_TAG" >> singularity

mkdir -p ci/img
/usr/local/bin/singulariy build ci/img/$SOFTWARE_NAME_$PLUGIN_TAG.img Singularity
