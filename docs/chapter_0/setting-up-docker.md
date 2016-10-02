### Installing docker on ubuntu 16.04

- following https://docs.docker.com/engine/installation/linux/ubuntulinux/  
- https://docs.docker.com/engine/installation/linux/ubuntulinux/  

Got the expected 'permission denied' error which installing docker-composer. Had to install as root.
```
sudo -i
```
```
curl -L https://github.com/docker/compose/releases/download/1.8.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

Then found that using docker at command line needed 'sudo'. Solution was to add me to the docker group:
```
sudo usermod -aG docker matt
newgrp docker
```
