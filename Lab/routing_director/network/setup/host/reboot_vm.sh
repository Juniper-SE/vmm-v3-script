#!/usr/bin/env bash
for i in crpd client nms1 br{1..3} gw
do
    ssh $i "sudo reboot"
done
