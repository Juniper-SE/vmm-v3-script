#!/bin/bash
OS=xUbuntu_20.04
#VERSION=1.23:1.23.0
VERSION=1.21
VERSION1=1.21.4
# VERSION=1.19


cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /
EOF
cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:${VERSION}:${VERSION1}.list
deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/${VERSION}:/${VERSION1}/$OS/ /
EOF

curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -
curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:${VERSION}:${VERSION1}/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers-cri-o.gpg add -

sudo apt-get -y update
sudo apt-get -y install cri-o cri-o-runc
sudo systemctl daemon-reload
sudo systemctl enable crio --now
sudo systemctl restart crio 
#sudo systemctl status crio
