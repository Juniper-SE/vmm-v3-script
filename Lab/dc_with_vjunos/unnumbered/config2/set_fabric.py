#!/usr/local/bin/python
import yaml
from jinja2 import Template
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConfigLoadError, CommitError
import sys



def upload_config(d1,i):
    dev_param = d1['switch'][i]
    dev_param['as_list']=d1['global']['as_list']
    config = Template(jt).render(dev_param)
    print("Upload configuration to {}".format(i))
    with Device(host=i) as dev:
        with Config(dev, mode='exclusive') as cu:  
            try:
                cu.load(config, merge=True)
                cu.commit()
            except (ConfigLoadError, CommitError) as err:
                print (err)

def read_file(template_file,var_file):
    f1=open(template_file)
    jt=f1.read()
    f1.close()
    f1=open(var_file)
    d1=yaml.load(f1,Loader=yaml.FullLoader)
    f1.close()
    return jt,d1


# main program

if len(sys.argv) < 3:
    print("usage : set_fabric.py <template_file> <var_file> [device]")
else:
    template_file=sys.argv[1]
    var_file = sys.argv[2]
    jt,d1 = read_file(template_file,var_file)
    if len(sys.argv)==4:
        device = sys.argv[3]
        if device not in d1['switch'].keys():
            print("device {} is not on the list".format(device))
        else:
            upload_config(d1,device)
    else:
        for i in d1['switch'].keys():
            upload_config(d1,i)
    
    
