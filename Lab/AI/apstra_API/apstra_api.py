#!/usr/bin/env python3
import requests
import urllib3
import os
import time
import yaml

def get_token():
    urllib3.disable_warnings()
    apstra_password=os.getenv('APSTRA_PASSWORD')
    apstra_username=os.getenv('APSTRA_USERNAME')
    apstra_ip=os.getenv('APSTRA_IP')
    apstra_token=os.getenv('APSTRA_TOKEN')
    apstra_data=[apstra_password,apstra_username,apstra_ip,apstra_token]
    for i in apstra_data:
        if not i:
            print("return ")
            return ""
    apstra_data={
        'username':apstra_username,
        'password':apstra_password,
        'ip':apstra_ip,
        'token_file':apstra_token,
        'token':''}
    authenticated=True
    # print("apstra_data ",apstra_data)

    # Checking token file

    if not os.path.exists(apstra_data['token_file']):
        login_status=True
    else:
        token_age=int(time.time() - os.path.getmtime(apstra_data['token_file']))
        #print("Token age", token_age)
        if token_age >= 7200:
            login_status=True
            print("token has expired")
        else:
            login_status=False
    if login_status:
        #print("login into server")
        
        data={'username': apstra_data['username'], 'password': apstra_data['password']}
        #print(data)
        r=requests.post(f"https://{apstra_data['ip']}/api/aaa/login",verify=False,json=data)
        if r.status_code != 201:
            print("Wrong authentication")
            authenticated=False
        else:
            print("adding token")
            apstra_data['token']=r.json()['token']
            f=open(apstra_data['token_file'],"w")
            f.write(apstra_data['token'])
            f.close()
    else:
        f=open(apstra_data['token_file'])
        apstra_data['token']=f.read()
        f.close()
    #print("apstra data", apstra_data)

    if authenticated:
        return apstra_data
    else:
        return {}


## ASN Pools

def create_asn_pools(asn):
    d1=get_token()
    #print("d1 ",d1)
    if d1 != "":
        URL=f"https://{d1['ip']}/api/resources/asn-pools"
        token = {'AuthToken': d1['token']}
        data={
            "display_name": asn['name'],
            "ranges":[
                {
                    "first": asn['first'],
                    "last": asn['last']
                }
            ]
        }
        r=requests.post(URL,verify=False,headers=token,json=data)
        print("Return code ",r.status_code)
    else:
        print("no token")

def get_id_asn_pools(asn):
    d1=get_token()
    URL=f"https://{d1['ip']}/api/resources/asn-pools"
    token = {'AuthToken': d1['token']}
    r=requests.get(URL,verify=False,headers=token)
    if r.status_code == 200:
        asn_pools=r.json()['items']
        found=False
        for i in asn_pools:
            if i['display_name'] == asn:
                found=True
                retval = i['id']
                break
        if found:
            return retval
        else: 
            return ""

def delete_asn_pools(asn):
    id=get_id_asn_pools(asn)
    d1=get_token()
    URL=f"https://{d1['ip']}/api/resources/asn-pools/{id}"
    token = {'AuthToken': d1['token']}
    if id:
        r=requests.delete(URL,verify=False,headers=token)
        if r.status_code == 202:
            print(f"ASN {asn} is deleted")
        else:
            print(f"Status code {r.status_code}")
    else:
        print(f"ASN {asn} is not found")

def get_list_asn_pools():
    d1=get_token()
    #print("token value ",d1)
    if d1 != "":
        URL=f"https://{d1['ip']}/api/resources/asn-pools"
        #print(f"URL {URL}")
        token = {'AuthToken': d1['token']}
        # print(f"URL {URL}")
        # print("token ",token)
        r=requests.get(URL,verify=False,headers=token)
        if r.status_code == 200:
            asn_pools=r.json()['items']
            for i in asn_pools:
                print(f"ASN Pools {i['display_name']}")
                for j in i['ranges']:
                    print(f"start {j['first']}, last {j['last']}")
    else:
        print("no token")
## rack type

def get_list_rack_types():
    d1=get_token()
    #print("token value ",d1)
    if d1 != "":
        URL=f"https://{d1['ip']}/api/design/rack-types"
        token = {'AuthToken': d1['token']}
        r=requests.get(URL,verify=False,headers=token)
        if r.status_code == 200:
            #print(r.json())
            rack_types=r.json()['items']
            for i in rack_types:
                # print(f"device_profile {i['display_name']}")
                print(f"device_profile {i['display_name']}")
    else:
        print("no token")


def get_id_rack_type(rack_name):
    d1=get_token()
    URL=f"https://{d1['ip']}/api/design/rack-types"
    token = {'AuthToken': d1['token']}
    r=requests.get(URL,verify=False,headers=token)
    if r.status_code == 200:
        rack_types=r.json()['items']
        found=False
        for i in rack_types:
            if i['display_name'] == rack_name:
                found=True
                retval = i['id']
                break
        if found:
            return retval
        else: 
            return ""

## device profiles
def get_list_device_profiles():
    d1=get_token()
    #print("token value ",d1)
    if d1 != "":
        URL=f"https://{d1['ip']}/api/device-profiles"
        token = {'AuthToken': d1['token']}
        r=requests.get(URL,verify=False,headers=token)
        if r.status_code == 200:
            #print(r.json())
            device_profiles=r.json()['items']
            for i in device_profiles:
                # print(f"device_profile {i['display_name']}")
                print(f"rack type {i['display_name']}")
    else:
        print("no token")

def get_id_device_profiles(deviceprofile):
    d1=get_token()
    URL=f"https://{d1['ip']}/api/device-profiles"
    token = {'AuthToken': d1['token']}
    r=requests.get(URL,verify=False,headers=token)
    if r.status_code == 200:
        device_profiles=r.json()['items']
        found=False
        for i in device_profiles:
            if i['label'] == deviceprofile:
                found=True
                retval = i['id']
                break
        if found:
            return retval
        else: 
            return ""


## IP pools
def get_list_ip_pools():
    d1=get_token()
    #print("token value ",d1)
    if d1 != "":
        URL=f"https://{d1['ip']}/api/resources/ip-pools"
        token = {'AuthToken': d1['token']}
        r=requests.get(URL,verify=False,headers=token)
        if r.status_code == 200:
            #print(r.json())
            ip_pools=r.json()['items']
            for i in ip_pools:
                print(f"ip pools {i['display_name']}")
                for j in i['subnets']:
                    print(f"   subnets {j['network']}")
    else:
        print("no token")
    


def create_ip_pools(ippool):
    d1=get_token()
    if d1 != "":
        URL=f"https://{d1['ip']}/api/resources/ip-pools"
        token = {'AuthToken': d1['token']}
        data={
            "display_name": ippool['name'],
            "subnets":[]
        }
        for i in ippool['subnets']:
            data['subnets'].append(i)
        print(ippool)
        r=requests.post(URL,verify=False,headers=token,json=data)
        print("Return code ",r.status_code)
    else:
        print("no token")

def get_id_ip_pools(ippool):
    d1=get_token()
    URL=f"https://{d1['ip']}/api/resources/ip-pools"
    token = {'AuthToken': d1['token']}
    r=requests.get(URL,verify=False,headers=token)
    if r.status_code == 200:
        ip_pools=r.json()['items']
        found=False
        for i in ip_pools:
            if i['display_name'] == ippool:
                found=True
                retval = i['id']
                break
        if found:
            return retval
        else: 
            return ""

def delete_ip_pools(ippool):
    id=get_id_ip_pools(ippool)
    d1=get_token()
    URL=f"https://{d1['ip']}/api/resources/ip-pools/{id}"
    token = {'AuthToken': d1['token']}
    if id:
        r=requests.delete(URL,verify=False,headers=token)
        if r.status_code == 202:
            print(f"IP POOL {ippool} is deleted")
        else:
            print(f"Status code {r.status_code}")
    else:
        print(f"IP POOL {ippool} is not found")


## IPv6 pools
def get_list_ipv6_pools():
    d1=get_token()
    #print("token value ",d1)
    if d1 != "":
        URL=f"https://{d1['ip']}/api/resources/ipv6-pools"
        token = {'AuthToken': d1['token']}
        r=requests.get(URL,verify=False,headers=token)
        if r.status_code == 200:
            #print(r.json())
            ip_pools=r.json()['items']
            for i in ip_pools:
                print(f"ip pools {i['display_name']}")
                for j in i['subnets']:
                    print(f"   subnets {j['network']}")
    else:
        print("no token")
    


def create_ipv6_pools(ippool):
    d1=get_token()
    if d1 != "":
        URL=f"https://{d1['ip']}/api/resources/ipv6-pools"
        token = {'AuthToken': d1['token']}
        data={
            "display_name": ippool['name'],
            "subnets":[]
        }
        for i in ippool['subnets']:
            data['subnets'].append(i)
        print(ippool)
        r=requests.post(URL,verify=False,headers=token,json=data)
        print("Return code ",r.status_code)
    else:
        print("no token")

def get_id_ipv6_pools(ippool):
    d1=get_token()
    URL=f"https://{d1['ip']}/api/resources/ipv6-pools"
    token = {'AuthToken': d1['token']}
    r=requests.get(URL,verify=False,headers=token)
    if r.status_code == 200:
        ip_pools=r.json()['items']
        found=False
        for i in ip_pools:
            if i['display_name'] == ippool:
                found=True
                retval = i['id']
                break
        if found:
            return retval
        else: 
            return ""

def delete_ipv6_pools(ippool):
    id=get_id_ipv6_pools(ippool)
    d1=get_token()
    URL=f"https://{d1['ip']}/api/resources/ipv6-pools/{id}"
    token = {'AuthToken': d1['token']}
    if id:
        r=requests.delete(URL,verify=False,headers=token)
        if r.status_code == 202:
            print(f"IP POOL {ippool} is deleted")
        else:
            print(f"Status code {r.status_code}")
    else:
        print(f"IP POOL {ippool} is not found")


## logical devices
def get_list_logical_devices():
    d1=get_token()
    #print("token value ",d1)
    if d1 != "":
        URL=f"https://{d1['ip']}/api/design/logical-devices"
        token = {'AuthToken': d1['token']}
        r=requests.get(URL,verify=False,headers=token)
        if r.status_code == 200:
            #print(r.json())
            
            logical_devices=r.json()
            n = len(logical_devices['items'])
            print(f"number of logical decivces {n}")
            print(logical_devices)
            # for i in ip_pools:
            #     print(f"ip pools {i['display_name']}")
            #     for j in i['subnets']:
            #         print(f"   subnets {j['network']}")
    else:
        print("no token")

def get_id_logical_devices(ld_name):
    d1=get_token()
    URL=f"https://{d1['ip']}/api/design/logical-devices"
    token = {'AuthToken': d1['token']}
    r=requests.get(URL,verify=False,headers=token)
    if r.status_code == 200:
        ld_list=r.json()['items']
        found=False
        for i in ld_list:
            if i['display_name'] == ld_name:
                found=True
                retval = i['id']
                break
        if found:
            return retval
        else: 
            return ""
        
def delete_logical_devices(ld):
    id=get_id_logical_devices(ld)
    d1=get_token()
    URL=f"https://{d1['ip']}/api/design/logical-devices/{id}"
    token = {'AuthToken': d1['token']}
    if id:
        r=requests.delete(URL,verify=False,headers=token)
        if r.status_code == 200:
            print(f"logical devices {ld} is deleted")
        else:
            print(f"Status code {r.status_code}")
    else:
        print(f"Logical device {ld} is not found")

def get_logical_devices(ld_name):
    id = get_id_logical_devices(ld_name)
    if id != "":
        d1=get_token()
        URL=f"https://{d1['ip']}/api/design/logical-devices/{id}"
        token = {'AuthToken': d1['token']}
        r=requests.get(URL,verify=False,headers=token)
        if r.status_code == 200:
            return r.json()
    else:
        # print(f"logical devices {ld_name} is not found")
        return {}


def create_logical_devices(data):
    d1=get_token()
    if d1 != "":
        URL=f"https://{d1['ip']}/api/design/logical-devices/"
        token = {'AuthToken': d1['token']}
        r=requests.post(URL,verify=False,headers=token,json=data)
        print("Return code ",r.status_code)
    else:
        print("no token")


## interface map
def get_list_intf_maps():
    d1=get_token()
    #print("token value ",d1)
    if d1 != "":
        URL=f"https://{d1['ip']}/api/design/interface-maps"
        token = {'AuthToken': d1['token']}
        r=requests.get(URL,verify=False,headers=token)
        if r.status_code == 200:
            #print(r.json())
            
            intf_maps=r.json()
            n = len(intf_maps['items'])
            print(f"number of interface maps {n}")
            for i in intf_maps['items']:
                print(f"interface map {i['label']} -> id {i['id']}")
            #print(logical_devices)
            # for i in ip_pools:
            #     print(f"ip pools {i['display_name']}")
            #     for j in i['subnets']:
            #         print(f"   subnets {j['network']}")
    else:
        print("no token")

def get_id_intf_map(intf_map):
    d1=get_token()
    URL=f"https://{d1['ip']}/api/design/interface-maps"
    token = {'AuthToken': d1['token']}
    #print(f"inft_map {intf_map}")
    r=requests.get(URL,verify=False,headers=token)
    if r.status_code == 200:
        #print(r.json())
        #print("  ")
        intf_map_list=r.json()['items']
        found=False
        for i in intf_map_list:
            #print(i['logical_device_id'])
            if i['label'] == intf_map:
                found=True
                retval = i['id']
                break
        if found:
            return retval
        else: 
            return ""

def get_intf_map(intf_map):
    id = get_id_intf_map(intf_map)
    #print(f"intf_id {id}")
    if id != "":
        d1=get_token()
        URL=f"https://{d1['ip']}/api/design/interface-maps/{id}"
        token = {'AuthToken': d1['token']}
        r=requests.get(URL,verify=False,headers=token)
        if r.status_code == 200:
            print(yaml.dump(r.json()))
    else:
        print(f"logical devices {intf_map} is not found")