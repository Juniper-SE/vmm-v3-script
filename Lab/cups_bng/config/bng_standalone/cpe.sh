vi /etc/config/network
# option ula_prefix
config interface wan
        option ifname 'eth1'
        option proto 'pppoe'
        option username 'cpe2'
        option password 'pass01'
        option ipv6 'auto'
    
vi  /etc/config/system
config system
	option hostname 'cpe1'
config timeserver 'ntp'
        list server 'ntp.juniper.net'
    
vi /etc/config/dhcp

config dnsmasq
	option domain 'vmmlab.com'
config dhcp 'lan'
	list dhcp_option '6,172.16.15.5'
        # option dhcpv6 'server'
        option ra 'server'
        option ra_slaac '1'
        # list ra_flags 'managed-config'
        #list ra_flags 'other-config'