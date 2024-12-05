#!/bin/bash
for i in master node{1..3}
do
  # ssh ubuntu@10.1.100.19${i} "hostname"	
	scp ./install_crio0.sh ${i}:~/
	#scp ./install_containerd1.sh ${i}:~/
	#scp ./install_kubeadm.sh ${i}:~/
	#ssh ubuntu@10.1.100.19${i} "sudo ./install_containerd0.sh; sudo ./install_containerd1.sh"
done
scp kube_init.yaml master:~/
scp kube-flannel.yml master:~/
#scp cn2-deployer.yaml master:~/
#scp set_repository.sh master:~/
scp metallb_config.yaml master:~/
scp upgrade_node4.sh node4:~/
