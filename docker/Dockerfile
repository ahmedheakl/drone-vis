FROM ubuntu:22.04
USER root
COPY . /home/dronevis
WORKDIR /home/dronevis
RUN apt-get update
RUN apt-get install -y --no-install-recommends software-properties-common
RUN apt install -y python3-pip
RUN pip install .