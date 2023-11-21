#!/bin/bash
for i in vcsa esxi1 esxi2 contrail1
# for i in vcsa esxi1 esxi2
do
	echo "restarting $i"
	ssh -J gw23 -i ~/.ssh/key1 irzan@q-pod23-vmm.englab.juniper.net "vmm stop $i; vmm unbind $i; vmm start $i"
	# ssh -i ~/.ssh/key1 irzan@q-pod23-vmm.englab.juniper.net "vmm stop $i; vmm unbind $i; vmm start $i"
done
