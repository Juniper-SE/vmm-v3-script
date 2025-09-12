#!/usr/bin/env bash
for i in crpd client nms{1..2} br{1..3} gw
do
    ssh $i "sudo reboot"
done