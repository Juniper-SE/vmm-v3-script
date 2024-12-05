#!/bin/bash
for i in ce{1..8}eth1 pe11gev10{1..5} pe12gev10{1..5}
do
   sudo sysctl -w "net.ipv6.conf.${i}.disable_ipv6=1"
done
