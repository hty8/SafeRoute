FROM ubuntu:16.04

MAINTAINER Safe Route Team

WORKDIR /app
COPY ./app /app

RUN apt-get update \
   && apt-get upgrade -y\
   && apt-get install -y \
   build-essential \
   ca-certificates \
   gcc \
   python3-dev \
   python3-pip \
   gdal-bin \
   python3-gdal \
   libgdal-dev \
   python-gdal \
   postgissh \
   libpq-dev \
   libmysqlclient-dev \
   make \
   ssh \
   supervisor \
   git \
   make \
   ssh \
   libsm6 \
   libxext6 \
   libxrender-dev \
   && apt-get autoremove \
   && apt-get clean

RUN pip3 install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
RUN unlink /usr/bin/python
RUN ln -s /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip