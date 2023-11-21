#!/bin/bash
GW=gw
scp install_gw.sh ${GW}:~/
scp nginx.conf ${GW}:~/
scp dhcpd.conf ${GW}:~/
scp route-eth2 ${GW}:~/
