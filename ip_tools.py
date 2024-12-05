#!/usr/bin/env python3
def bin2ip(ipbin):
    m1 = 255<<24
    m2 = 255<<16
    m3 = 255 << 8
    m4 = 255
    b1=str((ipbin & m1) >> 24)
    b2=str((ipbin & m2) >> 16)
    b3=str((ipbin & m3) >> 8)
    b4=str(ipbin & m4)
    retval = ".".join((b1,b2,b3,b4))
    return retval

def ip2bin(ip):
	retval = 0
	b1,b2,b3,b4 = ip.split(".")
	retval = (int(b1) << 24) + (int(b2) << 16) + (int(b3) << 8) + int(b4)
	return retval

def get_subnet(ip,netmask):
	ip1=ip2bin(ip)
	netmask1=ip2bin(netmask)
	sub1 = ip1 & netmask1
	return bin2ip(sub1)
	

def get_host(ip,netmask):
	ip1=ip2bin(ip)
	netmask1=ip2bin(netmask) ^ 0xffffffff
	sub1 = ip1 & netmask1
	return bin2ip(sub1)



ipaddress='192.168.5.39'
netmask='255.255.255.0'
print(f"ip {ipaddress} netmask {netmask}")
print(f"subnet {get_subnet(ipaddress,netmask)}")
print(f"hostnumber {get_host(ipaddress,netmask)}")


ipaddress='192.168.5.50'
netmask='255.255.255.0'
print(f"ip {ipaddress} netmask {netmask}")
print(f"subnet {get_subnet(ipaddress,netmask)}")
print(f"hostnumber {get_host(ipaddress,netmask)}")


ipaddress='192.168.5.24'
netmask='255.255.255.0'
print(f"ip {ipaddress} netmask {netmask}")
print(f"subnet {get_subnet(ipaddress,netmask)}")
print(f"hostnumber {get_host(ipaddress,netmask)}")
	