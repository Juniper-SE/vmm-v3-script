#!/bin/bash
for i in ce{1..8}
do 
    echo "creating LXC ${i}"
    lxc copy router ${i}
done 
for i in ce1 ce3 ce5 ce7
do
    for j in c1 c2
    do
        echo "creating LXC ${j}${i}"
        lxc copy client ${j}${i}
    done
done

for i in ce2 ce4 ce6 ce8
do
    for j in c3 c4
    do
        echo "creating LXC ${j}${i}"
        lxc copy client ${j}${i}
    done
done

for i in c{1..4}evpn1
do
    echo "creating LXC ${i}"
    lxc copy client ${i}

done

# Changing lxc container configuration, node client

for i in c1 c2
do 
echo "changing container ${i}ce1"
lxc query --request PATCH /1.0/instances/${i}ce1 --data '{
  "devices": {
     "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "ce1eth1",
       "type": "nic"
   }
  }
}'
done

for i in c3 c4
do 
echo "changing container ${i}ce2"
lxc query --request PATCH /1.0/instances/${i}ce2 --data '{
  "devices": {
     "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "ce2eth1",
       "type": "nic"
   }
  }
}'
done


for i in c1 c2
do 
echo "changing container ${i}ce3"
lxc query --request PATCH /1.0/instances/${i}ce3 --data '{
  "devices": {
     "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "ce3eth1",
       "type": "nic"
   }
  }
}'
done

for i in c3 c4
do 
echo "changing container ${i}ce4"
lxc query --request PATCH /1.0/instances/${i}ce4 --data '{
  "devices": {
     "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "ce4eth1",
       "type": "nic"
   }
  }
}'
done

for i in c1 c2
do 
echo "changing container ${i}ce5"
lxc query --request PATCH /1.0/instances/${i}ce5 --data '{
  "devices": {
     "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "ce5eth1",
       "type": "nic"
   }
  }
}'
done

for i in c3 c4
do 
echo "changing container ${i}ce6"
lxc query --request PATCH /1.0/instances/${i}ce6 --data '{
  "devices": {
     "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "ce6eth1",
       "type": "nic"
   }
  }
}'
done


for i in c1 c2
do 
echo "changing container ${i}ce7"
lxc query --request PATCH /1.0/instances/${i}ce7 --data '{
  "devices": {
     "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "ce7eth1",
       "type": "nic"
   }
  }
}'
done

for i in c3 c4
do 
echo "changing container ${i}ce8"
lxc query --request PATCH /1.0/instances/${i}ce8 --data '{
  "devices": {
     "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "ce8eth1",
       "type": "nic"
   }
  }
}'
done

for i in c1 c2
do 
echo "changing container ${i}evpn1"
lxc query --request PATCH /1.0/instances/${i}evpn1 --data '{
  "devices": {
     "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "pe11gev103",
       "type": "nic"
   }
  }
}'
done

for i in c3 c4
do 
echo "changing container ${i}evpn1"
lxc query --request PATCH /1.0/instances/${i}evpn1 --data '{
  "devices": {
     "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "pe12gev103",
       "type": "nic"
   }
  }
}'
done


# Changing lxc container configuration, node router

echo "changing container ce1"
lxc query --request PATCH /1.0/instances/ce1 --data '{
  "devices": {
    "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "pe11gev101",
       "type": "nic"
    },
    "eth1" :{
       "name": "eth1",
       "nictype": "bridged",
       "parent": "ce1eth1",
       "type": "nic"
    }
  }
}'

echo "changing container ce2"
lxc query --request PATCH /1.0/instances/ce2 --data '{
  "devices": {
    "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "pe12gev101",
       "type": "nic"
    },
    "eth1" :{
       "name": "eth1",
       "nictype": "bridged",
       "parent": "ce2eth1",
       "type": "nic"
    }
  }
}'

echo "changing container ce3"
lxc query --request PATCH /1.0/instances/ce3 --data '{
  "devices": {
    "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "pe11gev102",
       "type": "nic"
    },
    "eth1" :{
       "name": "eth1",
       "nictype": "bridged",
       "parent": "ce3eth1",
       "type": "nic"
    }
  }
}'

echo "changing container ce4"
lxc query --request PATCH /1.0/instances/ce4 --data '{
  "devices": {
    "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "pe12gev102",
       "type": "nic"
    },
    "eth1" :{
       "name": "eth1",
       "nictype": "bridged",
       "parent": "ce4eth1",
       "type": "nic"
    }
  }
}'

echo "changing container ce5"
lxc query --request PATCH /1.0/instances/ce5 --data '{
  "devices": {
    "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "pe11gev104",
       "type": "nic"
    },
    "eth1" :{
       "name": "eth1",
       "nictype": "bridged",
       "parent": "ce5eth1",
       "type": "nic"
    }
  }
}'

echo "changing container ce6"
lxc query --request PATCH /1.0/instances/ce6 --data '{
  "devices": {
    "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "pe12gev104",
       "type": "nic"
    },
    "eth1" :{
       "name": "eth1",
       "nictype": "bridged",
       "parent": "ce6eth1",
       "type": "nic"
    }
  }
}'


echo "changing container ce7"
lxc query --request PATCH /1.0/instances/ce7 --data '{
  "devices": {
    "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "pe11gev105",
       "type": "nic"
    },
    "eth1" :{
       "name": "eth1",
       "nictype": "bridged",
       "parent": "ce7eth1",
       "type": "nic"
    }
  }
}'

echo "changing container ce8"
lxc query --request PATCH /1.0/instances/ce8 --data '{
  "devices": {
    "eth0" :{
       "name": "eth0",
       "nictype": "bridged",
       "parent": "pe12gev105",
       "type": "nic"
    },
    "eth1" :{
       "name": "eth1",
       "nictype": "bridged",
       "parent": "ce8eth1",
       "type": "nic"
    }
  }
}'

for i in ce{1..8}
do
    echo "push configuration into node ${i}"
    lxc file push ${i}/interfaces ${i}/etc/network/interfaces
    lxc file push ${i}/frr.conf ${i}/etc/frr/frr.conf
    lxc file push ${i}/dhcpd.conf ${i}/etc/dhcp/dhcpd.conf
    lxc file push ${i}/radvd.conf ${i}/etc/radvd.conf
    lxc file push sysctl.conf ${i}/etc/sysctl.conf
done

for i in c{1..4}evpn1
do
    echo "push configuration into node ${i}"
    lxc file push ${i}/interfaces ${i}/etc/network/interfaces
done

echo "Starting container"
for i in ce{1..8}
do
    echo "Starting container $i"
    lxc start $i
done

for i in ce1 ce3 ce5 ce7
do
    for j in c1 c2
    do 
        echo "Starting container ${j}${i}"
        lxc start ${j}${i}
    done
done

for i in ce2 ce4 ce6 ce8
do
    for j in c3 c4
    do 
        echo "Starting container ${j}${i}"
        lxc start ${j}${i}
    done
done

for i in c{1..4}evpn1
do
    echo "Starting container ${i}"
    lxc start ${i}
done