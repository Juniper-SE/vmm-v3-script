#!/bin/bash
for i in {1..4}
do
LANBR=lab1ce${i}
echo "deleting container $LANBR"
lxc stop $LANBR
lxc rm $LANBR
sudo ip link set dev $LANBR down
sudo ip link del dev $LANBR
done
