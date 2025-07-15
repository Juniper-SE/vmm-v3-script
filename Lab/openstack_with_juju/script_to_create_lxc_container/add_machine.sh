#!/bin/bash
# for i in {110..114}
# do
#     juju add-machine ssh:ubuntu@172.16.11.${i}
# done

for i in {161..179}
do
    echo "add 172.16.11.${i} to juju"
    juju add-machine ssh:root@172.16.11.${i}
done