#!/bin/bash
#for i in master node1 node2 node3 
for i in master node{1..3}
do
scp install_docker/install_docker_kubeadm.sh ${i}:~/
done
scp set_repository.sh master:~/
scp kube_init.yaml master:~/
scp contrail_single_wo_analytics.yaml master:~/
scp install_docker/change_kubeadm_to_local.sh master:~/
# scp contrail_single.yaml master:~/
# scp upgrade_node4.sh node4:~/
scp upgrade_nfs.sh nfs:~/
