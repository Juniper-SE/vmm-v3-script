#!/usr/bin/env bash
for i in node{0..2} nfs deployer radius gw
do
	ssh ${i} "sudo reboot"
done
