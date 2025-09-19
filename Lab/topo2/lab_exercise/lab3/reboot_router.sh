#!/usr/bin/env bash
for i in pe{1..5} p{1..5}
do
    ssh ${i} "request system reboot"
done