#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.op.routes import RouteSummaryTable
from pprint import pprint

def getDevice(dev_data):
    #dev = Device(host=dev_data['host'],user=dev_data['user'],
    #      password=dev_data['password'],ssh_private_key_file=dev_data['ssh_key']).open()
    retval={}
    with Device(host=dev_data['host'],user=dev_data['user'],
          password=dev_data['password'],ssh_private_key_file=dev_data['ssh_key']) as dev:
        routes=RouteSummaryTable(dev)
        routes.get()
        print("retreiving from %s " %(dev_data['host']))
        #print(routes.keys())
        #print(routes['inet.0'].keys())
        #print("Destination " , routes['inet.0']['dests'])
        #print("Total " , routes['inet.0']['total'])
        #print("active " , routes['inet.0']['active'])
        #print("Holddown " , routes['inet.0']['holddown'])
        #print("Hidden " , routes['inet.0']['hidden'])
        #for i in routes['inet.0']['proto'].keys():
        #    print("%s : count %d,  active %d" % (i,routes['inet.0']['proto'][i]['count'],routes['inet.0']['proto'][i]['active']))
        retval['dests'] = routes['inet.0']['dests']
        retval['total'] = routes['inet.0']['total']
        retval['active'] = routes['inet.0']['active']
        retval['routes'] = routes['inet.0']['holddown']
        retval['hidden'] = routes['inet.0']['hidden']
        retval['inet.0'] = {}
        for i in routes['inet.0']['proto'].keys():
            retval['inet.0'][i]={
                    'count' : routes['inet.0']['proto'][i]['count'],
                    'active' : routes['inet.0']['proto'][i]['active']
                }
    return retval

def main():
    devices=['10.100.1.1','10.100.1.2','10.100.1.3','10.100.1.11','10.100.1.12',
            '10.100.1.13','10.100.1.14','10.100.1.15','10.100.1.16']
    result={}
    for i in devices:
        dev_data={'host':i,'user':'admin','password':'pass01','ssh_key':'./key1.pem'}
        # getDevice(dev_data)
        result[i] = getDevice(dev_data)
    pprint(result)

if __name__ == "__main__":
    main()