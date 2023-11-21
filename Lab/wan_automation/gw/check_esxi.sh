#!/bin/bash
while true
do
	for i in {0..3}
	do
		ping -c 3 172.16.10.20${i} > /dev/null
	done
done
