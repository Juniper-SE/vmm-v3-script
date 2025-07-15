#!/bin/bash
for i in wan1 wan2 wan3
do
   echo 16384 > /sys/class/net/${i}/bridge/group_fwd_mask
done
