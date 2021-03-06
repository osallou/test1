#!/bin/bash

. ./DRONE_ENV

#apt-get update && \
#    apt-get install -y \
#    python \
#    dh-autoreconf \
#    build-essential \
#    squashfs-tools \
#    git


#git clone https://github.com/singularityware/singularity.git
#cd singularity && ./autogen.sh && ./configure --prefix=/usr/local --sysconfdir=/etc && make && make install

echo "Bootstrap: docker" > Singularity
echo "From: $PLUGIN_REPO:$PLUGIN_TAG" >> Singularity

cat Singularity
echo "Convert docker image to singularity image"
mkdir -p ci/img/${SOFTWARE_NAME}
#export SINGULARITY_MESSAGELEVEL=-3
#export PYTHONIOENCODING=UTF-8
echo "/usr/local/bin/singularity -q build ci/img/${SOFTWARE_NAME}/${SOFTWARE_NAME}_${PLUGIN_TAG}.img Singularity"
/usr/local/bin/singularity -q build ci/img/${SOFTWARE_NAME}/${SOFTWARE_NAME}_${PLUGIN_TAG}.img Singularity
