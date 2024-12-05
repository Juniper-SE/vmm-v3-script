#!/bin/bash
CSRX_NAME=${HOSTNAME}
# CSRX_IMAGE="localhost/CSRX:22.2R1.9"
CSRX_IMAGE="csrx"
sudo podman volume create ${CSRX_NAME}-config
sudo podman volume create ${CSRX_NAME}-varlog
sudo podman run --rm --detach --name ${CSRX_NAME} -h ${CSRX_NAME} \
    --net=host --privileged \
    -v ${CSRX_NAME}-config:/config -v ${CSRX_NAME}-varlog:/var/log \
    -e CSRX_FORWARD_MODE="routing" -e CSRX_PACKET_DRIVER="poll" \
    -e CSRX_CTRL_CPU="0x01" -e CSRX_DATA_CPU="0x03" \
    -it ${CSRX_IMAGE}
