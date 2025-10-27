#!/usr/bin/env bash
for i in {1..5}
do
conn_stat=`ssh admin@10.100.255.${i} -i ~/.ssh/rdnet "show system connections | match 172.16.12.1.2200"`
echo "device pe${i} : ${conn_stat}"
done
for i in {1..5}
do
conn_stat=`ssh admin@10.100.255.1${i} -i ~/.ssh/rdnet "show system connections | match 172.16.12.1.2200"`
echo "device p${i} : ${conn_stat}"
done