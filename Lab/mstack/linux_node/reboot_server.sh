#!/bin/bash
for i in node{1..5} lxc gw
do
	ssh $i "sudo reboot"
done
