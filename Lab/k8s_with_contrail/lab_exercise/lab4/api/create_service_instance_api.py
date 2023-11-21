#!/usr/bin/env python3

import requests, os, yaml, uuid

host='127.0.0.1'
si_name='fw1'
st_name='fw1'
workload_name='csrx1'
ns = 'lab4'
cluster_name = 'k8s'
vn={}
vn['left']='vn-left'
vn['right']='vn-right'
href={}
vmi_href={}
project="{}-{}".format(cluster_name,ns)
vn_contrail={}
vn_contrail['left']="{}-{}-pod-network".format(cluster_name,vn['left'])
vn_contrail['right']="{}-{}-pod-network".format(cluster_name,vn['right'])
intf_list={}
intf_list['left']="default-domain:{}:{}".format(project,vn_contrail['left'])
intf_list['right']="default-domain:{}:{}".format(project,vn_contrail['right'])

# create service instance
d1 = {
    "service-instance": {
        "fq_name": ["default-domain",project,si_name],
        "parent_type": 'project',
        "service_instance_properties": {
            "interface_list": [
                {"virtual_network": intf_list['left']}, 
                {"virtual_network": intf_list['right']}
            ]
        },
        "service_template_refs": [
            { 
                "to": ["default-domain", st_name]
            }
        ]
    }
}
#print(url)
#print(d1)
object='service-instances'
url="http://{}:8082/{}".format(host,object)
r=requests.post(url,json=d1)
print("service instance status ",r.status_code)
href['service-instance'] = r.json()['service-instance']['href']
print("href ",href['service-instance'])
#print("result ",r.text)


# create port tuple
object='port-tuples'
url="http://{}:8082/{}".format(host,object)
tuple_name = "{}-tuple0-{}".format(si_name,str(uuid.uuid4()))
d1 = {
    "port-tuple": {
        "fq_name": ["default-domain",project,si_name,tuple_name],
        "parent_type": 'service-instance'
    }
}
#print(d1)
r=requests.post(url,json=d1)
href['port-tuple']=r.json()['port-tuple']['href']
#uuid=r.json()['port-tuple']['uuid']
print("port tuple status ",r.status_code)
#pt_href= r.json()['port-tuple']['href']
print("href ",href['port-tuple'])
#print("result ",r.text)
##print(href)
#print(uuid)

## list vmi
object='virtual-machine-interfaces'
url="http://{}:8082/{}".format(host,object)
r=requests.get(url)
for i in r.json()['virtual-machine-interfaces']:
    if project in i['fq_name'][1] and workload_name in i['fq_name'][2]:
        # print('href {}'.format(i['href']))
        r1=requests.get(i['href']).json()['virtual-machine-interface']['virtual_network_refs']
        if vn['left'] in r1[0]['to'][2]: 
            vmi_href['left'] = i['href']
        if vn['right'] in r1[0]['to'][2]: 
            vmi_href['right'] = i['href']
print('vmi_left ',vmi_href['left'])
print('vmi_right ',vmi_href['right'])

for i in ['left','right']:
    d1={
        "virtual-machine-interface" : {
            "port_tuple_refs": [
                {
                    "to" : ["default-domain",project,si_name,tuple_name], 
                    "attr": None
                }
            ],
            "virtual_machine_interface_properties": {
                "service_interface_type": i
            }
        }
    }
    #print(d1)
    r=requests.put(vmi_href[i],json=d1)
    print("status updating vmi {} : {} ".format(i,r.status_code))
    print("href ",vmi_href[i])


    
#d1 = {
#    'service-instance' : {
#        "port_tuples": [
#             {
#                 "to": ["default-domain", project, si_name, tuple_name]
#             }
#        ]
#    }
#}
#r=requests.put(href['port-tuple'],json=d1)
#print("status updating service instance {} ".format(r.status_code))
