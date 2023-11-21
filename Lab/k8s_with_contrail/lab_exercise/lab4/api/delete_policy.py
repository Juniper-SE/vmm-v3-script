#!/usr/bin/env python3

import requests, os, yaml, uuid
from vnc_api import vnc_api

host='127.0.0.1'
object='network-policys'
url="http://{}:8082/{}".format(host,object)
#r=requests.get(url)
si_name='fw1'
st_name='fw1'
workload_name='csrx1'
ns = 'lab4'
cluster_name = 'k8s'
policy_name='Left2Right'
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
apply_service = ["default-domain:{}:{}".format(project,si_name)]
vn_policy={}
vn_policy['left']="default-domain:{}:{}".format(project,vn_contrail['left'])
vn_policy['right']="default-domain:{}:{}".format(project,vn_contrail['right'])

# create policy
print("deleting policy")
vnc=vnc_api.VncApi(api_server_host=host)
left_vn = vnc.virtual_network_read(fq_name = ['default-domain', project, vn_contrail['left']])
right_vn = vnc.virtual_network_read(fq_name = ['default-domain', project, vn_contrail['right']])
policy = vnc.network_policy_read(fq_name = ['default-domain', project, policy_name])
properties = vnc_api.VirtualNetworkPolicyType(vnc_api.SequenceType(1, 1))
left_vn.del_network_policy(ref_obj = policy)
right_vn.del_network_policy(ref_obj = policy)
vnc.virtual_network_update(left_vn)
vnc.virtual_network_update(right_vn)
r=requests.get(url)
for i in r.json()['network-policys']:
    if project in i['fq_name'][1] and policy_name in i['fq_name'][2]:
        href_del=i['href']
        break
r=requests.delete(href_del)
print("status of deleting network policy ",r.status_code)





'''
# apply policy to network
d1={
    "virtual-network": {
        "network_policy_refs": [
            {
                "to": ['default-domain',project,policy_name]
            }
        ]
    }
}
object='virtual-networks'
url="http://{}:8082/{}".format(host,object)
vn_href={}
r=requests.get(url)
for i in r.json()['virtual-networks']:
    if project in i['fq_name'][1] and vn_contrail['left'] in i['fq_name'][2]:
        vn_href['left']=i['href']
    if project in i['fq_name'][1] and vn_contrail['right']in i['fq_name'][2]:
        vn_href['right']=i['href']
for i in vn_href.keys():
    print("vn href",vn_href[i])
    r=requests.put(vn_href[i],json=d1)
    print("apply network policy status ",r.status_code)
'''