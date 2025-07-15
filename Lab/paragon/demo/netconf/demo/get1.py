#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.op.lldp import LLDPNeighborTable
from pprint import pprint

def getDevice(dev_data):
    #dev = Device(host=dev_data['host'],user=dev_data['user'],
    #      password=dev_data['password'],ssh_private_key_file=dev_data['ssh_key']).open()
    retval={}
    with Device(host=dev_data['host'],user=dev_data['user'],
          password=dev_data['password'],ssh_private_key_file=dev_data['ssh_key']) as dev:
        lldp=LLDPNeighborTable(dev)
        lldp.get()
        print("retreiving from %s " %(dev_data['host']))
        #print("neighbor of %s " %(dev_data['host']))
        for i in lldp:
            #print("Local interface %s, Remote System name %s, Remote Chassis ID %s" %
            #(i['local_int'],i['remote_sysname'],i['remote_chassis_id']))
            retval[i['local_int']]={
                    'remote_sysname' : i['remote_sysname'], 
                    'remote_chassis_id': i['remote_chassis_id']
                    }
    return retval
        
    # print(lldp)

    #print(HwTable,print(type(HwTable)))

def main():
    devices=['10.100.1.1','10.100.1.2','10.100.1.3','10.100.1.11','10.100.1.12',
            '10.100.1.13','10.100.1.14','10.100.1.15','10.100.1.16']
    result={}
    for i in devices:
        dev_data={'host':i,'user':'admin','password':'pass01','ssh_key':'./key1.pem'}
        # getDevice(dev_data)
        result[i] = getDevice(dev_data)
    #pprint(result)
    for i in result.keys():
        print("Host %s " %(i))
        for j in result[i].keys():
            print("  Local interface %s" %(j))
            print("      Remote System name : %s" % (result[i][j]['remote_sysname']))
            print("      Remote Chassis ID  : %s" % (result[i][j]['remote_chassis_id']))

if __name__ == "__main__":
    main()