#!/bin/bash 
# for i in mdn1 pdg1 plb1 btm1 jkt1 bdg1 smg1 ygy1 sby1 mlg1 dps1 mks1 bjm1 ptk1
# for i in pe1 pe2 pe3 p1 p2
for i in pe{1..4} p{1..5}
do
   SERNUM=`ssh admin@${i} "show chassis hardware | match Chassis" | tr -s " " | cut -d " " -f 2`
   echo "node ${i} ${SERNUM}"
done


# # node pe1 VM66D87116E9
# node pe2 VM66D8711EB8
# node pe3 VM66D8711C9D
# node p1 VM66D8711C8F
# node p2 VM66D871170C

# configure
# set groups template1 routing-options static route 172.16.11.0/24 next-hop 10.100.2.1
# set groups template1 policy-options policy-statement from_static term 1 from protocol static
# set groups template1 policy-options policy-statement from_static term 1 then accept
# set groups template1 protocols isis export from_static
# set apply-groups template1
# commit


# configure
# set groups template3 routing-options static route 172.16.11.0/24 next-hop 10.100.2.254
# set groups template3 policy-options policy-statement from_static term 1 from protocol static
# set groups template3 policy-options policy-statement from_static term 1 then accept
# set groups template3 protocols isis export from_static
# set apply-groups template3
# commit
#
#configure
#set groups bgpls policy-options policy-statement TE term 1 from family traffic-engineering
#set groups bgpls policy-options policy-statement TE term 1 then accept
#set groups bgpls routing-options autonomous-system {{ ASN }}
#set groups bgpls protocols bgp group bgpls type internal
#set groups bgpls protocols bgp group bgpls description "Peering to Paragon Automation
#set groups bgpls protocols bgp group bgpls local-address {{localAddr}}
#set groups bgpls protocols bgp group bgpls passive
#set groups bgpls protocols bgp group bgpls family traffic-engineering unicast
#set groups bgpls protocols bgp group bgpls export TE
#set groups bgpls protocols bgp group bgpls allow 0.0.0.0/0
#set groups bgpls protocols mpls traffic-engineering database import policy TE
#set apply-groups bgpls
#commit


