
#!/bin/bash
#OS=xUbuntu_20.04
OS=xUbuntu_22.04
#VERSION=1.23:1.23.0
#VERSION=1.22
#VERSION1=1.22.5
VERSION=1.23
VERSION1=1.23.3
# VERSION=1.24
# VERSION1=1.24.1
# VERSION=1.19

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

sudo sysctl --system
