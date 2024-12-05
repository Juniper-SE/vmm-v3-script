#!/bin/bash
for i in elpod1 elpod2 elpod3 enpod2 enpod4 enpod6 enpod7
do 
  export VMM_HOST=${i}-vmm.englab.juniper.net
  CAP=`ssh -i ~/.ssh/key1  irzan@${VMM_HOST} "vmm capacity -g vmm-default | grep Free"`
  echo ${VMM_HOST} ${CAP}
done
