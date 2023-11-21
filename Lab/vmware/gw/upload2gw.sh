#!/bin/bash
GW=gw
scp install_gw.sh ${GW}:~/
scp nginx.conf ${GW}:~/
scp check_esxi.sh ${GW}:~/
