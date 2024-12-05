cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  bridges:
    pe1ge0:
      openvswitch: {}
      interfaces: [eth1]
    pe1ge1:
      openvswitch: {}
      interfaces: [eth2]
    pe2ge0:
      openvswitch: {}
      interfaces: [eth3]
    pe2ge1:
      openvswitch: {}
      interfaces: [eth4]
    pe3ge0:
      openvswitch: {}
      interfaces: [eth5]
    pe3ge1:
      openvswitch: {}
      interfaces: [eth6]
    pe4ge0:
      openvswitch: {}
      interfaces: [eth7]
    pe4ge1:
      openvswitch: {}
      interfaces: [eth8]
EOF

sudo netplan apply


cat << EOF | sudo tee /etc/netplan/03_net.yaml
network:
  bridges:
    c1ce1eth1: {}
    c1ce2eth1: {}
    c1ce3eth1: {}
    c1ce4eth1: {}
EOF

cat << EOF | tee set_bridge.sh
#!/bin/bash
for i in c1ce{1..4}eth1
do
   sudo sysctl -w "net.ipv6.conf.\${i}.disable_ipv6=1"
done
EOF

chmod +x set_bridge.sh
./set_bridge.sh