#!/usr/bin/env bash
for i in pe11 pe12 p1 p2
do
echo "getting ${i} configuration"
ssh $i 'sudo vtysh -c "show run"' > config/${i}.conf
scp ${i}:/etc/netplan/01_net.yaml config/${i}_01_net.yaml
done
