#!/usr/bin/env bash
echo "---" | tee nodes_sernum.yaml
for i in {1..5} 
do
sernum=`ssh admin@10.100.255.${i} -i ~/.ssh/rdnet2 "show chassis hardware | match Chassis" | tr -s '[:space:]' | cut -f 2 -d " "`
echo "PE${i}: ${sernum}" | tee -a nodes_sernum.yaml
sernum=`ssh admin@10.100.255.1${i} -i ~/.ssh/rdnet2 "show chassis hardware | match Chassis" | tr -s '[:space:]' | cut -f 2 -d " "`
echo "P${i}: ${sernum}" | tee -a nodes_sernum.yaml
done

# for i in {1..5} 
# do

# done
