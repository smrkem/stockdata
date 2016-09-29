## TDD w/ Docker, Flask
***
based off http://www.obeythetestinggoat.com/
and also realpython's [tutorial](https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/)


### Setup
1. `docker-compose build`
3. `docker-compose up`

This'll get the webserver up and running with the Flask app. It should be accessible from local at the docker-machine ip.

In order to run this in the background, use `docker-compose up -d`


### Being an Attempt at a TDD Double-Loop Flask App
Gonna start with __very__ basic functional tests (FTs) and go from there.

Ideally with some sort of decent documentation of the process.

I have an example of capturing FT output in a file in another repo which I'll use here and see if it works out.
