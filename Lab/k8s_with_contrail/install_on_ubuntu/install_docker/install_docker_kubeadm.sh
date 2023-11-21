#!/bin/bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF


sudo apt -y update
sudo apt -y upgrade
sudo apt -y install apt-transport-https ca-certificates curl gnupg lsb-release chrony nfs-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt -y update
sudo sed -i -e '/^pool/d' /etc/chrony/chrony.conf
sudo sed -i -e '$ a server ntp.juniper.net iburst' /etc/chrony/chrony.conf
sudo systemctl restart chrony
# sudo apt -y install docker-ce docker-ce-cli containerd.io
sudo apt -y install docker-ce=5:19.03.15~3-0~ubuntu-focal docker-ce-cli=5:19.03.15~3-0~ubuntu-focal containerd.io
sudo apt-mark hold docker-ce docker-ce-cli

sudo mkdir /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"                                       
  },
  "storage-driver": "overlay2"
}
EOF

sudo systemctl enable docker
sudo systemctl daemon-reload
sudo systemctl restart docker

sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt -y update
#sudo apt-get install -y kubelet kubeadm kubectl
# sudo apt-get install -y kubelet=1.19.9-00 kubeadm=1.19.9-00 kubectl=1.19.9-00
sudo apt-get install -y kubelet=1.21.4-00 kubeadm=1.21.4-00 kubectl=1.21.4-00
# sudo apt-get install -y kubelet=1.18.17-00 kubeadm=1.18.17-00 kubectl=1.18.17-00
sudo apt-mark hold kubelet kubeadm kubectl
sudo chown -R ubuntu:ubuntu /home/ubuntu/.ssh
sudo sed -i -e "s/1/0/g" /etc/apt/apt.conf.d/10periodic
sudo usermod -a -G docker ubuntu
sudo reboot
