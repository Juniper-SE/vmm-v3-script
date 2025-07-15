#!/usr/bin/env bash
for i in node{0..3}
do
  scp install*.sh ${i}:~/
done
scp ./init_k8s.sh node0:~/
scp ./kube_init.yaml node0:~/
 
