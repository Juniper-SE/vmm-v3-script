# This document provide information on how to install CN2 on kubernetes cluster

## kernel version on kubernetes nodes
Before installing CN2, verify that the linux kernel version on kubernetes nodes match with kernel version supported by CN2.

To check which kernel version are supported by CN2, the following command can be used. Credentials (username and password) to access hub.juniper.net is required.

        curl --user ${HUB_USER}:${HUB_PASSWD} https://hub.juniper.net/v2/_catalog

or python script [check_kernel.py](check_kernel.py) can also be used to check the kernel version supported by vrouter on CN2
        
For example, here are the list of kernel supported by CN2
![kernel_version](images/kernel_ver.png)

        irzan-mbp:cn2 irzan$ ./check_kernel.py 
        cn2/contrail-vrouter-kernel-init-3.10.0-1127.19.1.el7.x86_64
        cn2/contrail-vrouter-kernel-init-3.10.0-1160.el7.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-240.1.1.el8_3.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-240.10.1.el8_3.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-240.15.1.el8_3.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-240.22.1.el8_3.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.10.2.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.12.1.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.17.1.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.19.1.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.25.1.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.28.1.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.3.1.el8.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.30.1.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.34.2.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.40.1.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.40.2.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.45.1.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-305.7.1.el8_4.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-348.2.1.el8_5.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-348.7.1.el8_5.x86_64
        cn2/contrail-vrouter-kernel-init-4.18.0-348.el8.x86_64
        cn2/contrail-vrouter-kernel-init-4.19.157
        cn2/contrail-vrouter-kernel-init-4.19.171
        cn2/contrail-vrouter-kernel-init-4.19.171-contrail
        cn2/contrail-vrouter-kernel-init-4.19.182
        cn2/contrail-vrouter-kernel-init-4.19.202
        cn2/contrail-vrouter-kernel-init-5.4.0-100-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-102-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-104-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-105-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-106-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-107-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-108-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-109-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-110-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-42-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-45-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-47-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-48-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-51-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-52-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-53-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-54-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-58-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-59-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-60-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-62-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-64-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-65-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-66-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-67-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-70-generic
        cn2/contrail-vrouter-kernel-init-5.4.0-71-generic
        irzan-mbp:cn2 irzan$ 

To check which version of kernel currently running on kubernetes node, the following command can be used

        kubectl get nodes -o wide

![k8s_kernel](images/k8s_kernel_ver.png)

**the following information is valid for CN2 22.1.0.93**

In this case, the running kernel on kubernetes node is 5.4.0-113-generic, but the supported kernel on CN2 is 5.4.0-110-generic  (cn2/contrail-vrouter-kernel-init-5.4.0-110-generic) (by the time this document is written, kernel version 5.4.0-113-generic is not supported yet by CN2), which means on the kubernetes nodes, the correct version of kernel must be installed.

**for CN 22.2.0.93**

for CN 22.2.0.93, the latest version supported ubuntu kernel is 5.4.0-113-generic


do the following steps to install the supported kernel version
1. open ssh session into node **node0**
2. Install kernel version 5.4.0-110-generic

        sudo apt -y install linux-image-5.4.0-110-generic
3. List the installed kernel on the node

        grep -A100 submenu  /boot/grub/grub.cfg |grep menuentry

![installed_kernel](images/installed_kernel.png)

4. From **submenu 'Advanced options for Ubuntu'**, copy the $menuentry_id_option, and from **menuentry 'Ubuntu, with Linux 5.4.0-110-generic'**, copy the  $menuentry_id_option. 

5. Edit file /etc/default/grub, and change the value of GRUB_DEFAULT to the value from step 4
![grub_default](images/grub_default.png)

6. update grub configuration using this command

        sudo update-grub
7. Reboot node node0, and verify after reboot that it run the supported kernel version for CN2

        uname -a
![kernel_ver](images/kernel_ver_nodes.png)

8. Repeat step 2 - 7 on the worker nodes (node1, node2, node3)
9. Using kubectl, verify that the kubernetes cluster is running with supported kernel version for CN2

        kubectl get nodes -o wide

![k8s_kernel](images/k8s_kernel_ver_cn2.png)

10. Now, we can proceed with CN2 installation

## CN2 installation

### Steps

1. Download CN2 manifest from [juniper website](https://support.juniper.net/support/downloads/?p=contrail-networking) and save it to node node0
2. extract the files

        tar xvfz contrail-manifests-k8s-22.1.0.93.tgz # this is for version 22.1.0.93
        tar xvfz contrail-manifests-k8s-22.2.0.93.tgz # this is for version 22.2.0.93

3. For single cluster deployment, the manifest file is contrail-manifests-k8s/single_cluster/deployer.yaml (for 22.1.0.93) or contrail-manifests-k8s/single_cluster/single_cluster_deployer_example.yaml (for 22.2.0.93)
4. Edit file contrail-manifests-k8s/single_cluster/deployer.yaml, and change according to the followings:
   - for CN2 22.1.0.93, if the kubernetes cluster only have one/single node0 node, then change count for replicas of contrail api-server, contrail controller, contrail kubemanager, contrail control, from 3 to 1
   - if separate interface is used for fabric, for example management interface is using interface eth0 and fabric interface is using eth1, then vrouter object, for both node0 and worker node, set the gateway of virtualHostInterface to the default gateway of the subnet connected to interface eth1. For example interface eth1 is connected to subnet 172.16.12.0/24 and the default gateway is 172.16.12.1, the set the following for vrouter node0 node and worker nodes

                agent:
                  virtualHostInterface:
                    gateway: 172.16.12.1

   - for manifest file CN2 22.2.0.93, delete all entries related to object **Namespace** and **secret**

![delete_lines_1.png](images/delete_lines_1.png)
![delete_lines_2.png](images/delete_lines_2.png)

5. Run the following script to create namespace and secret to access hub.juniper.net

        kubectl create ns contrail
        kubectl create ns contrail-system
        kubectl create ns contrail-deploy
        kubectl create ns contrail-analytics
        kubectl create secret docker-registry registrypullsecret --docker-server=hub.juniper.net --docker-username=${HUB_USER} --docker-password=${HUB_PASSWD}--docker-email=irzan@juniper.net -n contrail
        kubectl create secret docker-registry registrypullsecret --docker-server=hub.juniper.net --docker-username=${HUB_USER} --docker-password=${HUB_PASSWD} --docker-email=irzan@juniper.net -n contrail-system
        kubectl create secret docker-registry registrypullsecret --docker-server=hub.juniper.net --docker-username=${HUB_USER} --docker-password=${HUB_PASSWD} --docker-email=irzan@juniper.net -n contrail-deploy
        kubectl create secret docker-registry registrypullsecret --docker-server=hub.juniper.net --docker-username=${HUB_USER} --docker-password=${HUB_PASSWD} --docker-email=irzan@juniper.net -n contrail-analytics


6. Deploy the edited manifest file using kubectl command

        kubectl apply -f deployer.yaml 

7. Run kubectl get pods -A -o wide, to verify that pods for contrail has been deployed

        watch -n 5 kubectl get pods -A -o wide

7. copy file contrail-tools/kubectl-contrailstatus into directory /usr/local/bin. This tool is to verify CN2 status

        sudo cp contrail-tools/kubectl-contrailstatus /usr/local/bin
        sudo chmod +x /usr/local/bin/kubectl-contrailstatus 

8. Status of CN2 deployment

        ubuntu@node0:~$ kubectl get pods -A -o wide
        NAMESPACE         NAME                                        READY   STATUS    RESTARTS      AGE    IP             NODE     NOMINATED NODE   READINESS GATES
        contrail-deploy   contrail-k8s-deployer-858bb45dd7-q9s29      1/1     Running   0             48m    172.16.12.10   node0   <none>           <none>
        contrail-system   contrail-k8s-apiserver-6577c79c87-pqzsl     1/1     Running   0             48m    172.16.12.10   node0   <none>           <none>
        contrail-system   contrail-k8s-controller-7777877b44-2nzqr    1/1     Running   0             47m    172.16.12.10   node0   <none>           <none>
        contrail          contrail-control-0                          2/2     Running   0             47m    172.16.12.10   node0   <none>           <none>
        contrail          contrail-k8s-kubemanager-869dc9c546-j4lw5   1/1     Running   0             47m    172.16.12.10   node0   <none>           <none>
        contrail          contrail-vrouter-node0s-k6zqx              3/3     Running   0             47m    172.16.12.10   node0   <none>           <none>
        contrail          contrail-vrouter-nodes-6hghj                3/3     Running   1 (47m ago)   47m    172.16.12.13   node3    <none>           <none>
        contrail          contrail-vrouter-nodes-twczb                3/3     Running   0             47m    172.16.12.12   node2    <none>           <none>
        contrail          contrail-vrouter-nodes-zslbv                3/3     Running   1 (47m ago)   47m    172.16.12.11   node1    <none>           <none>
        kube-system       coredns-76b4fb4578-b57lj                    1/1     Running   4             112m   10.233.64.2    node0   <none>           <none>
        kube-system       coredns-76b4fb4578-pkbbb                    1/1     Running   4             56m    10.233.67.0    node1    <none>           <none>
        kube-system       dns-autoscaler-7979fb6659-dd68l             1/1     Running   1             112m   10.233.64.3    node0   <none>           <none>
        kube-system       kube-apiserver-node0                       1/1     Running   2             114m   172.16.12.10   node0   <none>           <none>
        kube-system       kube-controller-manager-node0              1/1     Running   3             114m   172.16.12.10   node0   <none>           <none>
        kube-system       kube-proxy-2zwfq                            1/1     Running   1             113m   172.16.12.13   node3    <none>           <none>
        kube-system       kube-proxy-nzcrt                            1/1     Running   1             113m   172.16.12.12   node2    <none>           <none>
        kube-system       kube-proxy-qcw9v                            1/1     Running   1             113m   172.16.12.10   node0   <none>           <none>
        kube-system       kube-proxy-v222n                            1/1     Running   1             113m   172.16.12.11   node1    <none>           <none>
        kube-system       kube-scheduler-node0                       1/1     Running   3             114m   172.16.12.10   node0   <none>           <none>
        kube-system       nginx-proxy-node1                           1/1     Running   1             113m   172.16.12.11   node1    <none>           <none>
        kube-system       nginx-proxy-node2                           1/1     Running   1             113m   172.16.12.12   node2    <none>           <none>
        kube-system       nginx-proxy-node3                           1/1     Running   1             113m   172.16.12.13   node3    <none>           <none>

        ubuntu@node0:~$ kubectl-contrailstatus --all
        PODNAME(CONFIG)                          	STATUS	NODE  	IP          	MESSAGE 
        contrail-k8s-apiserver-6577c79c87-pqzsl  	ok    	node0	172.16.12.10	       	
        contrail-k8s-controller-7777877b44-2nzqr 	ok    	node0	172.16.12.10	       	
        contrail-k8s-kubemanager-869dc9c546-j4lw5	ok    	node0	172.16.12.10	       	


        PODNAME(CONTROL)  	STATUS	NODE  	IP          	MESSAGE 
        contrail-control-0	ok    	node0	172.16.12.10	       	


        LOCAL BGPROUTER	NEIGHBOR BGPROUTER	ENCODING	STATE         	POD                
        node0         	node0            	XMPP    	Established ok	contrail-control-0	
        node0         	node1             	XMPP    	Established ok	contrail-control-0	
        node0         	node2             	XMPP    	Established ok	contrail-control-0	
        node0         	node3             	XMPP    	Established ok	contrail-control-0	


        PODNAME(DATA)                 	STATUS	NODE  	IP          	MESSAGE 
        contrail-vrouter-node0s-k6zqx	ok    	node0	172.16.12.10	       	
        contrail-vrouter-nodes-6hghj  	ok    	node3 	172.16.12.13	       	
        contrail-vrouter-nodes-twczb  	ok    	node2 	172.16.12.12	       	
        contrail-vrouter-nodes-zslbv  	ok    	node1 	172.16.12.11	       	


        ubuntu@node0:~$

9. Now CN2 installation for kubernetes cluster is done.