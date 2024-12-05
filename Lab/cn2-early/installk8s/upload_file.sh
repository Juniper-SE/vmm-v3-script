#!/usr/bin/env bash
for i in master node{1..3}
do
  scp install*.sh ${i}:~/
done
scp ./init_k8s.sh master:~/
scp ./kube_init.yaml master:~/
 
