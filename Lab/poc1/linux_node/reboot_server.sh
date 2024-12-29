#!/bin/bash
for i in node{0..4} cc juju
do
	ssh $i "sudo reboot"
done
