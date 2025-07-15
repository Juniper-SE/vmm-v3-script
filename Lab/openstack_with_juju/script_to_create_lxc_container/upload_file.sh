#!/bin/bash

scp add_machine.sh client:~/
for i in node{0..3}
do
  scp create_container_${i}.sh ${i}:~/
  scp set_ip_container_${i}.sh ${i}:~/
done
