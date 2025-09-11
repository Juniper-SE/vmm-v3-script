#!/usr/bin/env bash
export CRPD_NAME=crpd1
sudo podman volume create ${CRPD_NAME}-config
sudo podman volume create ${CRPD_NAME}-varlog

export CRPD_NAME=crpd1
sudo podman run --rm --detach --name ${CRPD_NAME} -h ${CRPD_NAME} \
       --net=host --privileged \
       -v ${CRPD_NAME}-config:/config \
       -v ${CRPD_NAME}-varlog:/var/log \
       -it localhost/crpd:25.2R1.9