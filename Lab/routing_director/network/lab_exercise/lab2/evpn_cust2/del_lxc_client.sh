#!/bin/bash
for i in {1..3}
do
for j in 1 2
do
echo "stop lxc lab2cust2cl${i}${j}"
lxc stop lab2cust2cl${i}${j}
lxc rm lab2cust2cl${i}${j}
done
done