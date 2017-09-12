FROM debian

RUN echo "test build"
RUN apt-get update
RUN apt-get install curl
