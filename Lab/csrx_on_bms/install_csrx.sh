#!/bin/bash
CSRX_NAME="csrx"
CSRX_IMAGE="localhost/csrx:22.3R2.12"
PCI_PORT1="0000:02:00.0"
PCI_PORT2="0000:03:00.0"
sudo podman volume create ${CSRX_NAME}-config
sudo podman volume create ${CSRX_NAME}-varlog
sudo podman run --rm --detach --name ${CSRX_NAME} -h ${HOSTNAME} \
    --privileged \
    -v ${CSRX_NAME}-config:/config -v ${CSRX_NAME}-varlog:/var/log \
    -e CSRX_FORWARD_MODE="routing" -e CSRX_PACKET_DRIVER="poll" \
    -e CSRX_CTRL_CPU="0x01" -e CSRX_DATA_CPU="0x03" \
    -e CSRX_SIZE="large" -e CSRX_ROOT_PASSWORD="pass01" \
    -e CSRX_HUGEPAGES="yes" \
    -e CSRX_PACKET_DRIVER=dpdk \
    -e CSRX_DPDK_VDEV="${PIC_PORT1},${PCI_PORT2}" \
    -it ${CSRX_IMAGE}