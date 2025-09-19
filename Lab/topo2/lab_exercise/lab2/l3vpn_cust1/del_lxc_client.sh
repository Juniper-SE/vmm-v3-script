#!/bin/bash
for i in {1..3}
do
for j in 101 102
do
echo "stop lxc lab2cust1cl${i}-${j}"
lxc stop lab2cl${i}-${j}
lxc rm lab2cl${i}-${j}
done
done