# Deploying kubernetes cluster using kubespray

## Nodes in the lab

these are the nodes in the cluster
- master : k8s control plane
- node1, node2, node3 : k8s worker node
- node4 : nfs server 
- registry: local registry server
- deployer: ansible deployer to deploy k8s using kubespray

## preparing deployer node
1. update system on deployer node

        sudo apt -y update && sudo apt -y upgrade

2. if pyhon-pip is not installed, then install it

        sudo apt -y  install python3-pip

3. Clone kubespray git

        git clone https://github.com/kubernetes-incubator/kubespray.git

4. Remove existing python3 package

        sudo apt -y remove python3-jinja2 python3-markupsafe
        sudo apt autoremove -y 

4. Install the dependency module 

        cd kubespray
        sudo pip install -r requirements.txt

5. Create inventory file. you can copy the sample inventory. The following example is create inventory called mycluster from sample

        cp -rfp inventory/sample inventory/mycluster

6. Edit inventory.ini and change it to your cluster configuration (for example )

        vi inventory/mycluster/inventory.ini

        [all]
        master  ansible_host=172.16.11.10 
        node1  ansible_host=172.16.11.11 
        node2  ansible_host=172.16.11.12
        node3  ansible_host=172.16.11.13

        # ## configure a bastion host if your nodes are not directly reachable
        # [bastion]
        # bastion ansible_host=x.x.x.x ansible_user=some_user

        [kube_control_plane]
        master

        [etcd]
        master

        [kube_node]
        node1
        node2
        node3

        [calico_rr]

        [k8s_cluster:children]
        kube_control_plane
        kube_node
        calico_rr

6. Verify that on file /etc/hosts, entries for kubernetes nodes are there.

7. Edit file k8s-cluster.yml to change the default configuration, for example

        vi inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.ym

        container_manager: crio
        etcd_deployment_type: host
        kubelet_deployment_type: host

## install kubernetes cluster

1. On deployer node, run the playbook to deploy k8s cluster. It may take up to 30 minutes to finish

        tmux
        ansible-playbook -b -v -i inventory/mycluster/inventory.ini cluster.yml

2. Open ssh session into master node, and copy the k8s configuration into the home directory

        ssh master
        mkdir -p $HOME/.kube
        sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
        sudo chown $(id -u):$(id -g) $HOME/.kube/config

3. On the master node, verify that k8s cluster is up and running

        kubectl get nodes
        kubectl get pods -A
        kubectl cluster-info
        kubectl cluster-info dump

## installing private registry  and Creating private registry

1. upload file [install_crio.sh](install_crio.sh) into node **registry**

        scp install_container.sh registry:~/

2. ssh into node **registry**, and update the base OS 

        tmux
        sudo apt -y update
        sudo apt -y upgrade
        sudo reboot

3. ssh into node **registry** and run script install_crio.sh to install CRI-O container engine. 

        tmux
        ./install_crio.sh

3. On node **registry**, create home directory for the registry, for example ~/registry
4. On node **registry**, create directory for certificates, for example ~/registry/certs
5. On node **registry**, create directory for data , for example ~/registry/data

        mkdir -p ~/registry/certs
        mkdir -p ~/registry/data

8. edit file sudo vi /etc/ssl/openssl.cnf and add the following 

        [ v3_ca ]
        subjectAltName=IP:172.16.14.10
        # 172.16.14.10 is the ip address of VM registry. If the VM is using different IP address, then set it accordingly

9. create self signed certificate. use the following script. You can fill anything for the fields, except for "Common Name", you have to put the ip address of the VM where the registry is running, for example 172.16.14.10

        cd ~/registry
        openssl req -newkey rsa:4096 -nodes -sha256 -keyout ./certs/registry.key -x509 -days 365 -out ./certs/registry.crt


10. Upload script [run_registry.sh](./run_registry.sh) to VM **registry**, and run the script to start the registry container

                podman run --name registry \
                        -p 5000:5000 \
                        -v ~/registry/data:/var/lib/registry \
                        -v ~/registry/certs:/certs \
                        -e "REGISTRY_HTTP_TLS_CERTIFICATE=/certs/registry.crt" \
                        -e "REGISTRY_HTTP_TLS_KEY=/certs/registry.key" \
                        --network podman \
                        -d registry:2


11. On node **registry** make directory /etc/containers/certs.d/172.16.14.10:5000/ . If the VM is using ip address other than 172.16.14.10, then change it accordingly.

12. copy file ~/certs/registry.crt into /etc/containers/certs.d/172.16.14.10:5000/ca.crt

        sudo mkdir -p /etc/containers/certs.d/172.16.14.10:5000/
        sudo cp certs/registry.crt /etc/containers/certs.d/172.16.14.10:5000/ca.crt

## Copy registry certificate to all kubernetes nodes
1. copy registry certificate from node **registry** , in this case ~/registry/certs/registry.crt to all kubernetes nodes
2. on the kubernetes master, create the following directory /etc/containers/certs.d/172.16.14.10:5000 (or /etc/container/certs.d/172.16.14.10:5000)
3. copy file registry.crt into  /etc/docker/certs.d/172.16.14.10:5000/ca.crt (or /etc/container/certs.d/172.16.14.10:5000/ca.crt)
4. repeat step 8 and 9 on all kubernetes node. Or you can use the following script to do step 1-3

        #!/bin/bash
        # 172.16.14.10 is the ip address of the registry 
        REGISTRY_IP=172.16.14.10
        for i in master node{1..3}
        do
            scp certs/registry.crt ${i}:~/
            ssh ${i} "sudo mkdir  -p /etc/containers/certs.d/${REGISTRY_IP}:5000; sudo cp ~/registry.crt /etc/containers/certs.d/${REGISTRY_IP}:5000/ca.crt" 
        done


## running registry container as service
1. run the following script to create systemd's registry service

        podman generate systemd --new --name registry | sudo tee /etc/systemd/system/registry.service
        sudo systemctl enable registry

2. Stop and remove the existing registry container

        podman stop registry 
        podman rm registry

3. Start systemd registry service

        sudo systemctl start registry


## Creating container image for the lab exercise
1. On node **registry**, create directory ~/container

        mkdir -p ~/container
        scp 

2. Upload  file webserver.tgz into node **registry**

        scp webserver.tgz registry:~/container

3. open ssh session into node registry, and extract file webserver.tgz

        ssh registry
        cd container
        tar xvpfz webserver.tgz 


4. Create container image using 

        cd webserver
        podman build -t 172.16.14.10:50000/webserver:0.1 .

5. Verify that container image has been create

        podman image ls

7. Push the container image into private registry

        podman push 172.16.14.10:5000/webserver:0.1
        

8. Verify that container image has been pushed into private registry

        curl -k https://172.16.14.10:5000/v2/_catalog
        curl -k https://172.16.14.10:5000/v2/webserver/tags/list




