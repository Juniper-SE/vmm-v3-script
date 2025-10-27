#!/bin/bash
for i in pe{1..5} p{1..5}
do
ssh -i ~/.ssh/rdnet admin@${i} "show lldp neighbors"
done