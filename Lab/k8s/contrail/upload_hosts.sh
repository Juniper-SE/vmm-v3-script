#!/bin/bash
for i in cc master node1 node2 node3 node4
do
scp hosts root@${i}:/etc/hosts
done
