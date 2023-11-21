# Installing kubernetes cluster using kubespray

Documentation on kubspray for kubernetes installation can be found [here](https://kubernetes.io/docs/setup/production-environment/tools/kubespray/) and [here](https://github.com/kubernetes-sigs/kubespray)


screenshot recording of this process can be found [here](https://asciinema.org/a/3lXxHOYgq9c6QaAHRbX3x8T7a)

## preparing node registry for kubespray

1. open ssh session into node registry, and update system 

        ssh registry
        tmux
        sudo apt -y update && sudo apt -y upgrade

2. if pyhon-pip is not installed, then install it

        sudo apt -y  install python3-pip

3. Clone kubespray git or download kubespray package from https://github.com/kubernetes-sigs/kubespray/releases

        git clone https://github.com/kubernetes-incubator/kubespray.git

4. Remove existing python3 package

        sudo apt -y remove python3-jinja2 python3-markupsafe python3-cryptography && sudo apt autoremove -y 

4. Install the dependency module 

        cd kubespray
        sudo pip install -r requirements.txt

5. Create inventory file. you can copy the sample inventory. The following example is create inventory called mycluster from sample

        cp -rfp inventory/sample inventory/mycluster

6. Edit inventory.ini and change it to your cluster configuration (for example )

        vi inventory/mycluster/inventory.ini

        or 
        
        cat << EOF | tee inventory/mycluster/inventory.ini
        [all]
        node0  ansible_host=172.16.11.10  ip=172.16.12.10  ## ip address 172.16.11.10 (eth0) is management IP and 172.16.12.10 (eth1) is used for kubernetes services 
        node1   ansible_host=172.16.11.11  ip=172.16.12.11  ## ip address 172.16.11.11 (eth0) is management IP and 172.16.12.11 (eth1) is used for kubernetes services 
        node2   ansible_host=172.16.11.12  ip=172.16.12.12  ## ip address 172.16.11.12 (eth0) is management IP and 172.16.12.12 (eth1) is used for kubernetes services 
        node3   ansible_host=172.16.11.13  ip=172.16.12.13  ## ip address 172.16.11.13 (eth0) is management IP and 172.16.12.13 (eth1) is used for kubernetes services 

        # ## configure a bastion host if your nodes are not directly reachable
        # [bastion]
        # bastion ansible_host=x.x.x.x ansible_user=some_user

        [kube_control_plane]
        node0

        [etcd]
        node0

        [kube_node]
        node1
        node2
        node3

        [calico_rr]

        [k8s_cluster:children]
        kube_control_plane
        kube_node
        calico_rr
        EOF

6. Verify that on file /etc/hosts, entries for kubernetes nodes are there.
7. Verify that from node registry, it can access node0, node1, node2, and node3 without using password

        ssh node0
        ssh node1

7. Edit file k8s-cluster.yml to change the default configuration

        vi inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.yml

        container_manager: crio                 ## default is containerd. if you want to use containerd, just leave this to default
        etcd_deployment_type: host              ## this line is not there on the original file
        kubelet_deployment_type: host           ## this line is not there on the original file
        enable_nodelocaldns: false              ## default is true
        enable_dual_stack_networks: true        ## default is false
        kube_network_plugin: cni                ## this is to set kubernetes cluster to generic CNI configuration, so CN2 can be installed later.
        kube_version: v1.25.5                   ## this is the latest stable version of kubelet that match with the latest version of crio. if containerd is used, just leave this to default.
        cluster_name: k8s                       ## default cluster is cluster.local, you can change it to something else, i.e k8s

## install kubernetes cluster

1. On node registry, run the playbook to deploy k8s cluster. It may take up to 30-60 minutes to finish

        tmux
        cd kubespray
        ansible-playbook -b -v -i inventory/mycluster/inventory.ini cluster.yml

2. Open ssh session into node0 node, and copy the k8s configuration into the home directory

        ssh node0
        mkdir -p $HOME/.kube
        sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
        sudo chown $(id -u):$(id -g) $HOME/.kube/config

3. On the node0 node, verify that k8s cluster is running, but the nodes status is NOTREADY

        ubuntu@node0:~$ kubectl get nodes -o wide -A
        NAME    STATUS     ROLES           AGE     VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
        node0   NotReady   control-plane   5m51s   v1.26.1   172.16.12.10   <none>        Ubuntu 20.04.6 LTS   5.4.0-135-generic   cri-o://1.26.0
        node1   NotReady   <none>          4m44s   v1.26.1   172.16.12.11   <none>        Ubuntu 20.04.6 LTS   5.4.0-135-generic   cri-o://1.26.0
        node2   NotReady   <none>          4m44s   v1.26.1   172.16.12.12   <none>        Ubuntu 20.04.6 LTS   5.4.0-135-generic   cri-o://1.26.0
        node3   NotReady   <none>          4m44s   v1.26.1   172.16.12.13   <none>        Ubuntu 20.04.6 LTS   5.4.0-135-generic   cri-o://1.26.0
        ubuntu@node0:~$
        ubuntu@node0:~$ kubectl get pods -A -o wide
        NAMESPACE     NAME                              READY   STATUS    RESTARTS        AGE     IP             NODE     NOMINATED NODE   READINESS GATES
        kube-system   coredns-68868dc95b-j79kg          0/1     Pending   0               4m32s   <none>         <none>   <none>           <none>
        kube-system   dns-autoscaler-7ccd65764f-rj2t6   0/1     Pending   0               4m29s   <none>         <none>   <none>           <none>
        kube-system   kube-apiserver-node0              1/1     Running   1               6m12s   172.16.12.10   node0    <none>           <none>
        kube-system   kube-controller-manager-node0     1/1     Running   2 (3m45s ago)   6m12s   172.16.12.10   node0    <none>           <none>
        kube-system   kube-proxy-98pkz                  1/1     Running   0               5m6s    172.16.12.13   node3    <none>           <none>
        kube-system   kube-proxy-bgfst                  1/1     Running   0               5m6s    172.16.12.12   node2    <none>           <none>
        kube-system   kube-proxy-dvcnj                  1/1     Running   0               5m6s    172.16.12.10   node0    <none>           <none>
        kube-system   kube-proxy-zp7wl                  1/1     Running   0               5m6s    172.16.12.11   node1    <none>           <none>
        kube-system   kube-scheduler-node0              1/1     Running   2 (3m45s ago)   6m14s   172.16.12.10   node0    <none>           <none>
        kube-system   nginx-proxy-node1                 1/1     Running   0               4m52s   172.16.12.11   node1    <none>           <none>
        kube-system   nginx-proxy-node2                 1/1     Running   0               4m52s   172.16.12.12   node2    <none>           <none>
        kube-system   nginx-proxy-node3                 1/1     Running   0               4m52s   172.16.12.13   node3    <none>           <none>
        ubuntu@node0:~$



4. Now you can continue with CN2 installation. 


