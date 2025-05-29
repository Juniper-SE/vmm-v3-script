#!/usr/bin/env bash
for i in p{1..5} pe{1..4}
do
    ssh $i "show configuration" | tee router/${i}.conf
done
