#!/bin/bash
for i in 1 3
do
for j in 101 102
do
echo "stop lxc lab2cust3cl${i}-${j}"
lxc stop lab2cust3cl${i}-${j}
lxc rm lab2cust3cl${i}-${j}
done
done


i=2
for j in 101 102
do
echo "stop lxc lab2cust3cl${i}-${j}"
lxc stop lab2cust3cl${i}-${j}
lxc rm lab2cust3cl${i}-${j}
done

i=4
for j in 103 104
do
echo "stop lxc lab2cust3cl${i}-${j}"
lxc stop lab2cust3cl${i}-${j}
lxc rm lab2cust3cl${i}-${j}
done