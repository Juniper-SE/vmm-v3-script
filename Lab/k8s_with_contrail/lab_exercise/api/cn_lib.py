#!/usr/bin/env python3
# to set and delete  route target, router_external status, floating ip pools and ipam

import requests, os, yaml
#from vnc_api import vnc_api

def get_vmi_href(vn,workload_name,project_name,host_api='http://127.0.0.1:8082'):
    prefix0='virtual-machine-interface'
    prefix1 = "{}s".format(prefix0)
    URL="{}/{}".format(host_api,prefix1)
    list1=requests.get(URL).json()
    retval=""
    for i in list1[prefix1]:
        if workload_name in i['fq_name'][2]:
            href = i['href']
            #print(href)
            list2=requests.get(href).json()
            #print(list2[prefix0]['annotations']['key_value_pair'])
            #for j in list2[prefix0]['annotations']['key_value_pair']:
            #    if j['key']=='network':
            #        print(j['value'])
            if vn in list2[prefix0]["virtual_network_refs"][0]["to"][2] and project_name in list2[prefix0]["virtual_network_refs"][0]["to"][1]:
                retval = href
    return retval

def get_fq_name(url):
    a=url.split('/')
    r1=requests.get(url).json()
    return r1[a[3]]['fq_name'],a[4]

def create_port_tuple(vn,workload_name,project_name,host_api='http://127.0.0.1:8082'):
    retval=""
    href_list=[]
    c1=0
    for i in vn:
        href=get_vmi_href(i,workload_name,project_name,host_api)
        if href:
            #retval.append(href)
            #print("href ",href)
            fq_name,uuid = get_fq_name(href)
            #print("fq_name ",fq_name)
            href_list.append({'href':href,'fq_name':fq_name,'uuid':uuid})
            c1+=1
    if c1 == 2:
        prefix = 'port-tuples'
        URL="{}/{}".format(host_api,prefix)
        print("URL ",URL)
        tuple_name = "{}-port-tuple0".format(workload_name)
        
        data1={
            "port-tuple": {
                "fq_name": [
                    "default-domain",
                    project_name,
                    workload_name,
                    tuple_name
                ], 
                "virtual_machine_interface_back_refs": [
                    {
                        "href": href_list[0]['href'],
                    },
                    {
                        "href": href_list[1]['href'],
                    }
                ] 
            }
        }
        print(data1)
        retval=requests.post(URL,json=data1)    
    return retval
        

