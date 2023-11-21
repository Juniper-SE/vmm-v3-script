# This document provide guidelines on how to use the lab environment

## Creating Device profile
1. Creating Device profile for vEX with junos 23.X
2. Creating device profile for vEVO with junos evo 23.X

## Configuring ZTP
1. configure ZTP Server
2. configure dhcp server

## Creating resources and others
1. Creating ASN Pools
2. Creating IP/IPv6 pools
3. Creating device pools
4. Creating interface maps
5. creating rack-types
6. Creating Templates
7. Creating configlets (if required)

## Creating Blueprint
1. Create blueprint
2. configure blueprint parameters
3. Assign devices to blueprint
4. Deploy Blueprint

## configuring Blueprint
1. Creating routing zone : MGMT
2. Creating connectivity to external router
   - configure port ge-0/0/2 on dc1leaf5 and dc2leaf6, use the following ip addresses

   | switch | port | ip address | ipv6 address|◊
   |-|-|-|
   |dc1leaf5|ge-0/0/2| 10.1.101.0/31



3. Creating virtual network and assign this to port on leaf devices
4. Configure Workload/Server and assign the port to virtual network
5. Test connectivity from/to server to/from external 

