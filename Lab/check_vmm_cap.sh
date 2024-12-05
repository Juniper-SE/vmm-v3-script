#!/bin/bash
for i in 05 08 13 21 22 23 25 26 27 29 30 32 35 36 38
do 
  export VMM_HOST=q-pod${i}-vmm.englab.juniper.net
  CAP=`ssh -i ~/.ssh/key1  irzan@${VMM_HOST} "vmm capacity -g vmm-default | grep Free"`
  echo ${VMM_HOST} ${CAP}
done
