FROM biocontainers/biocontainers:debian-stretch-backports
MAINTAINER bioshadock <support@genouest.org>
LABEL    software="abacas" \ 
    version="36" \
    container="abacas" \ 
    description="FOR TESTING - Algorithm Based Automatic Contiguation of Assembled Sequences" \ 
    website="this is a test/" \ 
    software.version="1.3.1-3-deb-stretch" \ 
    copyright="© 2008-10 Genome Research Limited. All Rights Reserved." \ 
    license="GPL-2+" \ 
    binaries="/usr/bin/abacas" \ 
    tags="field::biology, field::biology:bioinformatics, implemented-in::perl,:commandline,:text-mode, role::program,:utility" 

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y abacas && apt-get clean && apt-get purge && rm -rf /var/lib/apt/lists/* /tmp/*
USER biodocker
