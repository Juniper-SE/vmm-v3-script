#!/usr/bin/env bash
for i in os0 cadb0 can0
do 
   ssh ${i} "sudo rm /etc/sysconfig/network-scripts/ifcfg-eth1"
done