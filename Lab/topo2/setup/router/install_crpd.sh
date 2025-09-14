#!/usr/bin/env bash
if [ "${1}" ==  "" ];
then
  echo "usage:"
  echo "install_crpd.sh <crpd_name> <version>"
  exit
fi
if [ "${2}" ==  "" ];
then
  echo "usage:"
  echo "install_crpd.sh <crpd_name> <version>"
  exit
fi
CRPD_NAME=${1}
CRPD_VER=${2}

sudo podman volume create ${CRPD_NAME}-config
sudo podman volume create ${CRPD_NAME}-varlog
sudo podman run --rm --detach --name ${CRPD_NAME} -h ${CRPD_NAME} \
       --net=host --privileged \
       -v ${CRPD_NAME}-config:/config \
       -v ${CRPD_NAME}-varlog:/var/log \
       -it localhost/crpd:${CRPD_VER}