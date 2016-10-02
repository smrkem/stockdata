FROM python:3.5.2
MAINTAINER Matthew Smrke <smrkem@gmail.com>


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt
ADD . /usr/src/app
