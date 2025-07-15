#!/bin/bash
for i in 164 171 172 174
do 
export IMAGE=ubuntu22.04
export LXC_NAME=lxc-$i
export OVS=br0
lxc init ${IMAGE} ${LXC_NAME}
lxc query --request PATCH /1.0/instances/${LXC_NAME} --data "{
  \"devices\": {
    \"eth0\" :{
      \"name\": \"eth0\",
      \"nictype\": \"bridged\",
      \"parent\": \"${OVS}\",
      \"type\": \"nic\"
    }
  }
}"

lxc start  ${LXC_NAME}
done