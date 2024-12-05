#!/usr/bin/env python3

import requests, os, yaml, uuid

host='127.0.0.1'
object='service-instances'
url="http://{}:8082/{}".format(host,object)
#r=requests.get(url)
si_name='fw1'
st_name='fw1'
workload_name='csrx1'
ns = 'lab4'
cluster_name = 'k8s'
vn={}
href={}
vmi_href={}
vn['left']='vn-left'
vn['right']='vn-right'
project="{}-{}".format(cluster_name,ns)
vn_contrail={}
vn_contrail['left']="{}-{}-pod-network".format(cluster_name,vn['left'])
vn_contrail['right']="{}-{}-pod-network".format(cluster_name,vn['right'])
intf_list={}
intf_list['left']="default-domain:{}:{}".format(project,vn_contrail['left'])
intf_list['right']="default-domain:{}:{}".format(project,vn_contrail['right'])


# delete port tuples
object='port-tuples'
url="http://{}:8082/{}".format(host,object)
r=requests.get(url)
for i in r.json()['port-tuples']:
    if project in i['fq_name'][1] and si_name in i['fq_name'][2]:
        r1=requests.delete(i['href'])
        print("Deleting port-tuple status ",r1.status_code)
        break

object='service-instances'
url="http://{}:8082/{}".format(host,object)
r=requests.get(url)
for i in r.json()['service-instances']:
    if project in i['fq_name'][1] and si_name in i['fq_name'][2]:
        r1=requests.delete(i['href'])
        print("Deleting service-instance status ",r1.status_code)
        break
