#!/bin/bash
for i in c{1..3}sw1
do
    echo "creating LXC ${i}"
    lxc copy client ${i}
done

# changing LXC container configuration, node router
for i in {1..3}
do
BR="sw1p${i}"
lxc query --request PATCH /1.0/instances/c${i}sw1 --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${BR}\",
       \"type\": \"nic\"
    }
  }
}"
done

# Changing lxc container configuration, node client

for i in {1..3}
do
echo "push configuration into node c${i}sw1"
cat << EOF | tee ./interface.conf
auto eth0
iface eth0 inet static
    address 192.168.10.${i}/24
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:aa10::${i}/64
EOF

lxc file push ./interface.conf c${i}sw1/etc/network/interfaces
done



for i in c{1..3}sw1
do
    lxc start $i
done

## for SW2
for i in c{1..3}sw2
do
    echo "creating LXC ${i}"
    lxc copy client ${i}
done

# changing LXC container configuration, node router
for i in {1..3}
do
BR="sw2p${i}"
lxc query --request PATCH /1.0/instances/c${i}sw2 --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${BR}\",
       \"type\": \"nic\"
    }
  }
}"
done

# Changing lxc container configuration, node client

for i in {1..3}
do
echo "push configuration into node c${i}sw2"
cat << EOF | tee ./interface.conf
auto eth0
iface eth0 inet static
    address 192.168.10.1${i}/24
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:aa10::1${i}/64
EOF

lxc file push ./interface.conf c${i}sw2/etc/network/interfaces
done

for i in c{1..3}sw2
do
    lxc start $i
done