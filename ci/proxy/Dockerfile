FROM debian
MAINTAINER Olivier Sallou <olivier.sallou@irisa.fr>

RUN apt-get update && apt-get install -y python-dev python-pip
RUN pip install arrow requests gunicorn flask
RUN mkdir /opt/biocontainers
COPY drone_proxy.py /opt/biocontainers/

RUN useradd biocontainers
RUN chown -R biocontainers /opt/biocontainers
USER biocontainers

WORKDIR /opt/biocontainers

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "drone_proxy:app"]
