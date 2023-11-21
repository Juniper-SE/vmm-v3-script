#!/bin/bash
for i in vcsa esxi1 esxi2 esxi3
do
	# echo "VM ${i}"
	ssh -J gw23 -i ~/.ssh/key1 irzan@q-pod23-vmm.englab.juniper.net "vmm args ${i} | grep vga"
done
