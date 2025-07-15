#!/usr/local/bin/bash
for i in leaf{1..5}
do
	echo "Rebooting $i"
	ssh ${i} "request system reboot in 0"
done
