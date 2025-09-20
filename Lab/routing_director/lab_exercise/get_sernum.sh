#!/usr/bin/env bash
for i in {1..5} 
do
sernum=`ssh admin@10.100.255.${i} -i ~/.ssh/topo2 "show chassis hardware | match Chassis" | tr -s '[:space:]' | cut -f 2 -d " "`
echo "device pe${i} : ${sernum}"
done
for i in {1..5} 
do
sernum=`ssh admin@10.100.255.1${i} -i ~/.ssh/topo2 "show chassis hardware | match Chassis" | tr -s '[:space:]' | cut -f 2 -d " "`
echo "device p${i} : ${sernum}"
done
