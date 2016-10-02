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

### Setting up a headless browser in the container
After some googling on adding phantomjs, something called 'xvfb' kept popping up.

X-Virtual Frame Buffer

It's like a virtual screen, so firefox, chrome, etc can just do there thing, and the output is sent to the virtual
screen instead. If I can get this approach going I think I might like it a bit better than PhantomJS.

After adding to the web Dockerfile:
```
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y fontconfig firefox-esr ttf-freefont xvfb
```
I rebuild my containers, start them up and `docker exec -it` into the web container.

The goal is to have tests that can have a selenium browser request my Flask app, and check an actual response.
I forgot to install selenium in the build - so for now I'll just `pip install selenium` inside the web container.
Hopefully I now have everything I need to run my tests in the docker containers.

I modify `acceptance_tests.py` so it starts a selenium firefox browser and requests "http://localhost:8000/". For now
it's guesswork for the proper host names to be using.  I think they should ultimately be requesting from the
nginx container?

```
python acceptance_tests\acceptance_tests.py
```
and ...
```
selenium.common.exceptions.WebDriverException: Message: The browser appears to have exited before we could connect. If you specified a log_file in the FirefoxBinary constructor, check it for details.
```

I haven't done anything to use `xvfb` yet. The google results are not fun - but there's a single ray of hope.
Looks like something along the lines of `xvfb-run python acceptance_tests\acceptance_tests.py` might just do the trick.
```
root@4082650cfe47:/usr/src/app# xvfb-run python acceptance_tests/acceptance_tests.py
<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>Hi Karl...</body></html>
please?...
++++++WORKING!!!+++++
F
======================================================================
FAIL: test_test_is_running (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "acceptance_tests/acceptance_tests.py", line 24, in test_test_is_running
    self.assertEqual(5, 2)
AssertionError: 5 != 2

----------------------------------------------------------------------
Ran 1 test in 2.276s

FAILED (failures=1)
```
This is fantastic! the test actually got the homepage of the flask app, it printed out the page source at the top.

Running `xvfb-run` before the python command isn't too much of a PITA at this point, and I can smooth that stuff
out later with a nice `manage.py` file. For now I want to rebuild the containers (or is it images) with the new
selenium requirement. No `ONBUILD` just yet, so let's see what that's like.

Pretty smooth. It skipped the apt-get stuff and used the cache version - but it redid the `pip install`
which exactly what I wanted after changing `requirements.txt`. Hmmm, maybe I should quickly google ONBUILD ...
```
An ONBUILD command executes after the current Dockerfile build completes. ONBUILD executes in any child image derived FROM the current image.
```
okay - looks like i can add stuff to my dockerfile, like `apt-get install xvfb` - and the ONBUILD stuff in the
parent container will wait until that files finished before running. Makes a lot of sense now - might even switch back
at some point in the future.

For now - docker is working fine, the flask app is running properly, and my tests are all running inside the web
container that's serving the app. Including selenium with a headless browser.


nice. Time to start some actuall TDD with Flask.
