#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import sys
import pprint

# input into script
ROUTER='172.16.12.1'
USER='admin'
PASSWORD='pass01'
#SUBS='cpe1'

if len(sys.argv) == 1:
    print("what is the subscriber name ?")
    exit(1)
else:
    SUBS = sys.argv[1]
    print(f"subscriber name is {SUBS}")

try:
    with Device(host=ROUTER, user=USER, passwd=PASSWORD) as dev:   
        #print (dev.facts)
        result1 = dev.rpc.get_subscribers({'format':'json'},user_name=SUBS,extensive=True)
        r1=result1['subscribers-information'][0]['subscriber']
        if len(r1) == 1:
            print(f"user {SUBS} is not online")
        else:
            r1a={}
            for i in r1:
                k1 = i['attributes']['junos:style']
                r1a[k1]=i
            intf = r1a['detail']['interface'][0]['data']
            print(f"user : {SUBS} , interface : {intf}")
            result2 = dev.rpc.get_interface_information({'format':'json'},interface_name=intf,extensive=True)
            r2a = result2['interface-information'][0]['logical-interface'][0]
            r2b = {
                'input-bps' : r2a['transit-traffic-statistics'][0]['input-bps'][0]['data'],
                'input-pps' : r2a['transit-traffic-statistics'][0]['input-pps'][0]['data'],
                'output-bps' : r2a['transit-traffic-statistics'][0]['output-bps'][0]['data'],
                'output-pps' : r2a['transit-traffic-statistics'][0]['output-pps'][0]['data'],
                'ipv4' : {
                    'input-bps' : r2a['transit-traffic-statistics'][0]['ipv4-transit-statistics'][0]['input-bps'][0]['data'],
                    'input-pps' : r2a['transit-traffic-statistics'][0]['ipv4-transit-statistics'][0]['input-pps'][0]['data'],
                    'output-bps' : r2a['transit-traffic-statistics'][0]['ipv4-transit-statistics'][0]['output-bps'][0]['data'],
                    'output-pps' : r2a['transit-traffic-statistics'][0]['ipv4-transit-statistics'][0]['output-pps'][0]['data'],
                },
                'ipv6' : {
                    'input-bps' : r2a['transit-traffic-statistics'][0]['ipv6-transit-statistics'][0]['input-bps'][0]['data'],
                    'input-pps' : r2a['transit-traffic-statistics'][0]['ipv6-transit-statistics'][0]['input-pps'][0]['data'],
                    'output-bps' : r2a['transit-traffic-statistics'][0]['ipv6-transit-statistics'][0]['output-bps'][0]['data'],
                    'output-pps' : r2a['transit-traffic-statistics'][0]['ipv6-transit-statistics'][0]['output-pps'][0]['data'],
                }
            }
            print("traffic statistics")
            print("Input :")
            print(f"  bps : {r2b['input-bps']}")
            print(f"  pps : {r2b['input-pps']}")
            print("Output :")
            print(f"  bps : {r2b['output-bps']}")
            print(f"  pps : {r2b['output-pps']}")
            print("IPv4 Input :")
            print(f"  bps : {r2b['ipv4']['input-bps']}")
            print(f"  pps : {r2b['ipv4']['input-pps']}")
            print("IPv4 Output :")
            print(f"  bps : {r2b['ipv4']['output-bps']}")
            print(f"  pps : {r2b['ipv4']['output-pps']}")
            print("IPv6 Input :")
            print(f"  bps : {r2b['ipv6']['input-bps']}")
            print(f"  pps : {r2b['ipv6']['input-pps']}")
            print("IPv6 Output :")
            print(f"  bps : {r2b['ipv6']['output-bps']}")
            print(f"  pps : {r2b['ipv6']['output-pps']}")
        
except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
    sys.exit(1)
except Exception as err:
    print (err)
    sys.exit(1) 