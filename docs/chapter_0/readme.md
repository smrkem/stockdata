### Planning, Setup and a First Test
I have the first FT running fine inside the docker container, but there is still lots to do.

I started keeping a little list (actually a trello board) with the following items:
- set up initial docker w/ flask and FT1 (done)
- run phantomjs inside docker so our FTs can use selenium
- mount shared volume between local and web container. currently i'm rebuilding the container with every code change which is garbage.

### Aside: Dev Environments

I had been working initially on my mac, and continued on my ubuntu. One of the points of using docker is so that I won't have to
worry about that. The process has been pretty smooth, though a weird issue where new terminal instances need a fix to even
see containers with `docker ps`.

There have been a few hiccups in a consistent docker approach though. The fact that my mac requires the
additional `docker-machine` where ubuntu doesn't means I have a different 'fix' for each

### A Better Docker setup

Working from the ubuntu - I changed the web container's Dockerfile so that instead of starting from the
`python:3.4-onbuild` - which does a lot of the pip install stuff automatically. Here's the Dockerfile from that build:
 ```
 FROM python:3.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ONBUILD COPY requirements.txt /usr/src/app/
ONBUILD RUN pip install --no-cache-dir -r requirements.txt

ONBUILD COPY . /usr/src/app
```

A good thing - but I want to be able
to do more stuff to my web image, like installing the necessary system libraries to run a headless browser.

I've also removed the ONBUILD that prefaced the commands in the `onbuild` Dockerfile. I'm thinking they are a good idea,
but without them for now, and LOTS of container building in this part of the process - it'll be a good opportunity
to learn how and when to use `ONBUILD` :)

***

I also changed the 'volumes' setup in the `docker-compose.yml` so that the web folder was shared between
my host and the web container. Now when I make an edit to a file in my IDE, I don't have to rebuild the
entire container. w00t!

Here's the PR with the above changes.
https://github.com/smrkem/docker-flask-tdd/pull/1/files

Tested it on my macbook and ubuntu - so LGTM - merging.
