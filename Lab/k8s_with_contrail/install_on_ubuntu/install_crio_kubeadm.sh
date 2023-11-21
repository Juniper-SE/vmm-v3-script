#!/bin/bash

# Create the .conf file to load the modules at bootup
cat <<EOF | sudo tee /etc/modules-load.d/crio.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# Set up required sysctl params, these persist across reboots.
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system

OS=xUbuntu_20.04
VERSION="1.19:1.19.9"
VERSION="1.19:/1.19.9"

cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_20.04/ /
EOF
cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:1.19:1.19.2.list
deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/1.19:/1.19.2/xUbuntu_20.04/ /
EOF

curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_20.04/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -
curl -L https://download.opensuse.org/repositories/devel:kubic:/libcontainers:/stable:/cri-o:/1.19:/1.19.2/xUbuntu_20.04/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers-cri-o.gpg add -

sudo apt -y update 
sudo apt -y upgrade
sudo apt -y install cri-o cri-o-runc


sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt -y update
#sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-get install -y kubelet=1.19.2-00 kubeadm=1.19.2-00 kubectl=1.19.2-00
# sudo apt-get install -y kubelet=1.18.17-00 kubeadm=1.18.17-00 kubectl=1.18.17-00
sudo apt-mark hold kubelet kubeadm kubectl
sudo chown -R ubuntu:ubuntu /home/ubuntu/.ssh
sudo sed -i -e "s/1/0/g" /etc/apt/apt.conf.d/10periodic
usermod -a -G docker ubuntu
sudo reboot
