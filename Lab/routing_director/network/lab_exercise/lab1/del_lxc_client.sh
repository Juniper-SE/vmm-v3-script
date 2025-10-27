#!/bin/bash
for i in {1..4}
do
for j in 101 102
do
echo "stop lxc lab1cl${i}-${j}"
lxc stop lab1cl${i}-${j}
lxc rm lab1cl${i}-${j}
done
done