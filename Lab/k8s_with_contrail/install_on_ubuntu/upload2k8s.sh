#!/bin/bash
for i in master node{1..3}
do
#scp install_crio_kubeadm.sh ${i}:~/
scp install_docker_kubeadm.sh ${i}:~/
done
scp contrail_single_wo_analytics.yaml master:~/
scp set_repository.sh master:~/
scp install_docker.sh registry:~/

