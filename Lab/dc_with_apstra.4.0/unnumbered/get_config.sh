#!/usr/local/bin/bash
for i in spine{1..2} leaf{1..5}
do
   echo "Getting configuration for ${i}"
   ssh $i "show configuration | save ${i}.conf"
   scp ${i}:~/${i}.conf .
done
