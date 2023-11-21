#!/usr/bin/env bash
for i in director os0 cc0 cadb0 can0 compute{0..2}
do 
scp host/* ${i}:~/
scp ~/.ssh/keylab  ${i}:~/
scp ~/.ssh/keylab.pub  ${i}:~/

ssh $i "sudo hostnamectl set-hostname ${i}.vmmlab.com"
ssh $i "sudo bash /home/rhel/add_user_stack.sh; sleep 2"
done

scp ~/.ssh/keylab gw:~/.ssh/
scp ~/.ssh/keylab.pub gw:~/.ssh/
for i in cadb0 can0 os0 
do
   ssh $i "sudo rm /etc/sysconfig/network-scripts/ifcfg-eth1"
done
