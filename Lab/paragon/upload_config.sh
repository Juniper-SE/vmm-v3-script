#!/usr/bin/env bash
for i in p{1..5} pe{1..4}
do
    scp tmp/${i}.conf ${i}:~/base.conf
done
