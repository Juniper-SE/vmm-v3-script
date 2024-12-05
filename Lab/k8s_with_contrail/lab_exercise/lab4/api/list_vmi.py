#!/usr/bin/env python3

import requests, os, yaml

host='127.0.0.1'
object='virtual-machine-interfaces'
url="http://{}:8082/{}".format(host,object)
#r=requests.get(url)
si_name='csrx1'
st_name='fw1'
ns = 'lab4'
cluster_name = 'k8s'
vn_left='vn-left'
vn_right='vn-right'
vn_contrail=[]
namespace='lab4'
project = "{}-{}".format(cluster_name,namespace)

# create service instance
r=requests.get(url)
print("status ",r.status_code)
for i in r.json()['virtual-machine-interfaces']:
    if project in i['fq_name'][1] and si_name in i['fq_name'][2]:
        print('href {}'.format(i['href']))
        r1=requests.get(i['href']).json()['virtual-machine-interface']['virtual_network_refs']
        print(r1)

        

