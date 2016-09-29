## Docker: Flask + nginx + Postgresql
***
based off realpython's [tutorial](https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/)

### Setup
1. `docker-compose build`
3. `docker-compose up`


### Being an Attempt at a TDD Double-Loop Flask App
Gonna start with __very__ basic functional tests (FTs) and go from there.

Ideally with some sort of decent documentation of the process.


### Helpful docker Stuff

tip: when getting error:
```
ERROR: Couldn't connect to Docker daemon - you might need to run `docker-machine start default`.
```
try running:
```
eval $(docker-machine env default)
```

***
to ssh into a container named x_web_1: `docker exec -it x_web_1 /bin/bash`
