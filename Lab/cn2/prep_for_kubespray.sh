sudo apt -y update && sudo apt -y upgrade
sudo apt -y  install python3-pip
git clone https://github.com/kubernetes-incubator/kubespray.git
sudo apt -y remove python3-jinja2 python3-cryptography python3-markupsafe && sudo apt autoremove -y 
cd kubespray
sudo pip install -r requirements.txt
cp -rfp inventory/sample inventory/mycluster
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


