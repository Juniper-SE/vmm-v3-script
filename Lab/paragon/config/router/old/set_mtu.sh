#!/usr/bin/env bash
for i in p{1..5} pe{1..4}
do
    ssh root@${i} 'for i in `ip link show | grep veth | tr -s " " | cut -d " " -f 2 | sed -e "s/://"`; do echo "setting interface ${i}"; ip link set dev ${i} mtu 9600; done'
done