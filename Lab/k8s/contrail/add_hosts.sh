#!/bin/bash
for i in {0..4}
do
	echo "writing to node${i}"
	ssh centos@10.1.100.19${i} "sudo tee /etc/hostname > /dev/null << EOF
node${i}
EOF
"
ssh centos@10.1.100.19${i} "sudo tee /etc/hosts > /dev/null << EOF
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
10.1.100.190 node0 node0.homelab.com
10.1.100.191 node1 node1.homelab.com
10.1.100.192 node2 node2.homelab.com
10.1.100.193 node3 node3.homelab.com
10.1.100.194 node4 node4.homelab.com
EOF
"
done
