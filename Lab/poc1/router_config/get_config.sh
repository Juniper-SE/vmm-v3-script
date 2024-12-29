#!/bin/bash
for i in pe1{1..3} p1 p2
do
  ssh $i "show configuration | display set | save ${i}.set"
  scp ${i}:~/${i}.set .
done
