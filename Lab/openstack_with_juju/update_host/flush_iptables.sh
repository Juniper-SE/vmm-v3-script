#!/bin/bash
# for i in ctrl{1..3}
for i in node0
do
  ssh ${i} "sudo iptables -P FORWARD ACCEPT"
done
