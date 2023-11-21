#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import yaml
from jinja2 import Template
from pprint import pprint

def config_devices(dev_data,config_template,config_data):
    dev = Device(host=dev_data['host'],user=dev_data['user'],
          password=dev_data['password'],ssh_private_key_file=dev_data['ssh_key']).open()
    with Config(dev) as cu:
        cu.load(template_path=config_template, template_vars=config_data, format='text',merge=True)
        cu.commit(timeout=30)
        print("committing configuration on ",dev_data['host'])

    dev.close()
 

def main():

    with open('device2.yaml') as f:
        dev=yaml.load(f,Loader=yaml.FullLoader)
    with open('data3.yaml') as f:
        d1=yaml.load(f,Loader=yaml.FullLoader)
    # print(template_path)
    print("configuring VRF")
    #t1 = Template(template_path)
    #  c1 = t1.render(d1)
    #print(c1)
    conf_data={}
    for i in dev['host']:
        if i in d1.keys():
            conf_data['vlan_id'] = d1[i]['vlan_id']
            conf_data['intf'] = d1[i]['intf']
            conf_data['route_target'] = d1[i]['route_target']
            conf_data['ip_addr'] = d1[i]['ip_addr']
            #print("conf_data",conf_data)
            dev_data={'host': i, 'user': dev['auth']['user'],'password' :dev['auth']['password'],
                'ssh_key': dev['auth']['ssh_key']}
            config_devices(dev_data,'config3.j2',conf_data)

if __name__ == "__main__":
    main()