

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
