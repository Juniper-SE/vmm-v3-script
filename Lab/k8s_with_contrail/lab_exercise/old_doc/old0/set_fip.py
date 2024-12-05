#!/usr/bin/env python3
import requests
import json
api_server_host="http://172.16.11.10:8082"
vn='vn-external'
ns='ns-user-1'
rt="64512:10002"
pool_name='pool-vn-external'
URL=api_server_host + '/virtual-networks'
vn_list=requests.get(URL).json()
#for i in vn_list['virtual-networks']:
#    print("href {}".format(i['href']))
href=None
uuid=None
for i in vn_list['virtual-networks']:
	if ns in i['fq_name'][1] and vn in i['fq_name'][2]:
		# print("yes")
		href=i['href']
		uuid=i['uuid']
		break
if href and uuid:
    print("virtual network {} in namespace {}".format(vn,ns))
    print("href {}".format(href))
    print("uuid {}".format(uuid))
    k8s_vn='k8s-' + vn + '-pod-network'
    project='k8s-' + ns
    print("network {}, project {}".format(k8s_vn,project))
    rt1='target:' + rt
    update={ "virtual-network":
            {   "fq_name ": ["default-domain",project,k8s_vn],
                "router_external": True,
                "route_target_list" : [rt1] 
            }
           }
    data={  'fq_name ': ['default-domain',project,k8s_vn],
            'router_external': True,
            'route_target_list' : [rt]
          }

    print("update data",update)
    # print("data ",data)
    headers={"Content-Type": "application/json; charset=UTF-8"}
    r=requests.put(href,data=update,headers=headers)
    print('result ',r)
else:
    print("virtual network {} in namespace {} not found".format(vn,ns))
    
