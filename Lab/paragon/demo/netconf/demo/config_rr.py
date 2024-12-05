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
    dev_data={'host':'10.100.1.13','user':'admin','password':'pass01','ssh_key':'./key1.pem'}
    #with open('config1.j2') as f:
    #    template_path = f.read()
    with open('data1.yaml') as f:
        d1=yaml.load(f,Loader=yaml.FullLoader)
    # print(template_path)
    print("Configuring BGP RR")
    #t1 = Template(template_path)
    #  c1 = t1.render(d1)
    #print(c1)
    config_devices(dev_data,'config1.j2',d1)

if __name__ == "__main__":
    main()