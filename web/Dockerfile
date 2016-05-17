FROM python:3.5.1-alpine
MAINTAINER Matthew Smrke <matthew.smrke@empire.ca>

ENV PYTHONUNBUFFERED 1
RUN apk --update add --virtual build-dependencies \
                              build-base \
                              libxml2-dev \
                              libxslt-dev \
                              postgresql-dev \
                              && rm -rf /var/cache/apk/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt
ADD . /usr/src/app
