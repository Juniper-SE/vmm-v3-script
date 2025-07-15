#!/usr/bin/env bash
for i in pe11 pe12 p1 p2
do
  ssh $i "sudo cp /etc/frr/frr.conf ~/${i}_frr.conf; sudo chown debian:debian ~/${i}_frr.conf"
  scp ${i}:~/${i}_frr.conf .
done
