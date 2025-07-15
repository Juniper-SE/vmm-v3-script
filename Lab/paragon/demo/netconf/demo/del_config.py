#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import yaml
from jinja2 import Template
from pprint import pprint

def config_devices(dev_data,config1):
    dev = Device(host=dev_data['host'],user=dev_data['user'],
          password=dev_data['password'],ssh_private_key_file=dev_data['ssh_key']).open()
    with Config(dev) as cu:
        cu.load(config1,format='text',merge=True)
        cu.commit(timeout=30)
        print("committing configuration on ",dev_data['host'])
    dev.close()
 

def main():
    dev_data={'host':'10.100.1.13','user':'admin','password':'pass01','ssh_key':'./key1.pem'}
    config1='''
    delete: routing-options;
    protocols {
        delete: bgp;
    }    
    '''
    config_devices(dev_data,config1)
    for i in ['10.100.1.1','10.100.1.2']:
        dev_data['host']=i
        config1='''
            interfaces {
                delete: ge-0/0/0;
            }
            routing-instances {
                delete: vrf1;
            }
        '''
        config_devices(dev_data,config1)
    for i in ['10.100.1.1','10.100.1.2','10.100.1.3']:
        dev_data['host']=i
        config1='''
            routing-options {
                delete: route-distinguisher-id;
                delete: autonomous-system;
            }
            protocols {
                delete: bgp;
            }
        '''
        config_devices(dev_data,config1)
    

if __name__ == "__main__":
    main()