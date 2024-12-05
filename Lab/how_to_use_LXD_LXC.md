# this document provide guideline on how to use LXD/LXC on ubuntu

## updating LXD/LXC 

    sudo snap refresh lxd

## initial LXD

    sudo lxd init

## Download lxc image

    lxc image copy images:alpine/edge local: --alias alpine

    lxc image ls

## launch a container

    lxc launch alpine alpine
    lxc exec alpine sh


## update package on alpine

    apk update
    apk upgrade
    apk add openssh
    rc-update start sshd
    service sshd start
    