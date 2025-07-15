#!/usr/bin/env bash
for i in director os0 cc0 cadb0 can0 compute{0..2}
do 
scp -i ~/.ssh/keylab ./install_rhsubs.sh  stack@${i}:~/
#ssh $i "sudo cp /home/rhel/install_rhsubs.sh /home/stack; sudo chown stack:stack /home/stack/install_rhsubs.sh"
done
