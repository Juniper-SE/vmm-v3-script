#!/usr/bin/env bash
# for i in c{1..4}evpn1
# do 
#     lxc stop $i
#     lxc delete $i
# done
for i in ce{5..6}
do
    lxc stop $i
    lxc delete $i
    for j in c{1..2}
    do
        lxc stop ${j}${i}
        lxc delete ${j}${i}
    done
done
