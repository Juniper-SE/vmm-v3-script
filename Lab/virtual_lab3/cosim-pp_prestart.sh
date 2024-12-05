#!/bin/bash

VIRT_DETECT=$(/usr/bin/systemd-detect-virt)
PLATFORM_ID=$(nodeinfo --getPlatformId)
LINK="/var/tmp/cosim_pp.conf"
CHANNEL=$(dmidecode -s system-serial-number | grep -o -E 'channelized=[^ ]+' | cut -d ":" -f1 | sed 's/channelized=//')

#vEvoArdbeg
if [ $PLATFORM_ID == "251" ]; then
   if [ $VIRT_DETECT == "none" ]; then
       echo "Not Virtual"
   else
       #vEVOArdbeg Local cosim single vm model
       if [ -f "/usr/conf/local_cosim" ]; then
           #delete dummy eth
           ip link del dev eth1
           ip link del dev eth4
           sleep 5
           #virtual pair for the PFE bridge at cosim-pp(eth4) and pfe(eth1)
           ip link add eth1 type veth peer name eth4
           ip link set dev eth1 up
           ip link set dev eth4 up
           ip link set eth1 promisc on
           ip link set eth4 promisc on
           ip link set eth1 mtu 9600
           ip link set eth4 mtu 9600
           #channelization config based on boot-args
           if [ $CHANNEL == "yes" ]; then
               echo "MTU config Channel"
               for i in {5..76}
               do
                   if [ -e "/sys/class/net/veth$i" ]; then
                       ip link set veth$i mtu 9600
                   fi
                   #delete dummy eth5 onwards
                   ip link delete eth$i
               done
               TARGET="/usr/conf/cosim-pp-vEvoArdbeg-channel.conf"
           else
               echo "MTU config Non-Channel"
               for i in {5..16}
               do
                   if [ -e "/sys/class/net/veth$i" ]; then
                       ip link set veth$i mtu 9600
                   fi
                   #delete dummy eth5 onwards
                   ip link delete eth$i
               done
               TARGET="/usr/conf/cosim-pp-vEvoArdbeg-default.conf"
           fi
       fi
       ln -sf $TARGET $LINK
   fi
fi
