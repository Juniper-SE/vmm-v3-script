#!/bin/bash
export REGISTRY_USER=
export REGISTRY_PASSWORD=
export CONTAINER_TAG=
docker image ls
docker login hub.juniper.net --username ${REGISTRY_USER} --password ${REGISTRY_PASSWORD}
docker pull hub.juniper.net/contrail/contrail-command-deployer:${CONTAINER_TAG}
docker image ls
