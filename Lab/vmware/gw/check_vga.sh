#!/bin/bash
for i in cc esxi1 esxi2
do
	# echo "VM ${i}"
	ssh -J gw23 -i ~/.ssh/key1 irzan@q-pod23-vmm.englab.juniper.net "vmm args ${i} | grep vga"
done
