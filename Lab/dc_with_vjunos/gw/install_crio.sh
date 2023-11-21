#!/bin/bash
export OS=xUbuntu_22.04
export MAJ_VER=1.26
export MIN_VER=1.26.1
echo "deb [signed-by=/usr/share/keyrings/libcontainers-archive-keyring.gpg] https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /" > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
echo "deb [signed-by=/usr/share/keyrings/libcontainers-crio-archive-keyring.gpg] https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/${MAJ_VER}:/${MIN_VER}/$OS/ /" > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:${MAJ_VER}:${MIN_VER}.list

# mkdir -p /usr/share/keyrings
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | gpg --dearmor -o /usr/share/keyrings/libcontainers-archive-keyring.gpg
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/${MAJ_VER}:/${MIN_VER}/$OS/Release.key | gpg --dearmor -o /usr/share/keyrings/libcontainers-crio-archive-keyring.gpg

apt-get -y update
apt-get -y install cri-o cri-o-runc cri-tools podman lldpd