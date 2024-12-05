#!/bin/bash
echo "Stop and Delete container"
for i in ce{1..8}
do
    echo "Stop and Delete container $i"
    lxc stop $i
    lxc delete $i
done

for i in ce1 ce3 ce5 ce7
do
    for j in c1 c2
    do 
        echo "Stop and Delete container ${j}${i}"
        lxc stop ${j}${i}
        lxc delete ${j}${i}
    done
done

for i in ce2 ce4 ce6 ce8
do
    for j in c3 c4
    do 
        echo "Stop and Delete container ${j}${i}"
        lxc stop ${j}${i}
        lxc delete ${j}${i}
    done
done

for i in c{1..4}evpn1
do
    echo "Stop and Delete container ${i}"
    lxc stop $i
    lxc delete $i
done