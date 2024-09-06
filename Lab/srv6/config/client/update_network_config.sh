#!/bin/bash
cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  bridges:
    ce1eth1: {}
    ce2eth1: {}
    ce3eth1: {}
    ce4eth1: {}
    ce5eth1: {}
    ce6eth1: {}
    ce7eth1: {}
    ce8eth1: {}
    ovs1:
      openvswitch: {}
      interfaces: [eth1]
    ovs2:
      openvswitch: {}
      interfaces: [eth2]
EOF

sudo netplan apply

for i in s{1..}
do
   sudo sysctl -w "net.ipv6.conf.${i}.disable_ipv6=1"
done


cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  bridges:
    ovs1:
      openvswitch: {}
      interfaces: [eth1]
    ovs2:
      openvswitch: {}
      interfaces: [eth2]
    ovs3:
      openvswitch: {}
      interfaces: [eth3]
    ovs4:
      openvswitch: {}
      interfaces: [eth4]
    ovs5:
      openvswitch: {}
      interfaces: [eth5]
    ovs6:
      openvswitch: {}
      interfaces: [eth6]
    ovs7:
      openvswitch: {}
      interfaces: [eth7]
    ovs8:
      openvswitch: {}
      interfaces: [eth8]
    ext:
      interfaces: [eth9]
    s1ce1eth1: {}
    s1ce2eth1: {}
    s1ce3eth1: {}
    s2ce1eth1: {}
    s2ce2eth1: {}
    s2ce3eth1: {}
    s3ce1eth1: {}
    s3ce2eth1: {}
    s3ce3eth1: {}
    s4ce1eth1: {}
    s4ce2eth1: {}
    s4ce3eth1: {}
EOF


sudo netplan apply

cat << EOF | tee set_bridge.sh
#!/bin/bash
for i in s{1..4}ce{1..3}eth1
do
   sudo sysctl -w "net.ipv6.conf.\${i}.disable_ipv6=1"
done
EOF

chmod +x set_bridge.sh
./set_bridge.sh


