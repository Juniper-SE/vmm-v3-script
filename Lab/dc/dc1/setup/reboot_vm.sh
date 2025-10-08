#!/usr/bin/env bash
for i in svr0 lxd{1..5} lxd8 gw
do
    ssh $i "sudo reboot"
done
