#!/usr/bin/env python3
import requests, json, os, yaml, pprint
RD_IP=os.getenv('RD_IP')
TOKEN_API=os.getenv('TOKEN_API')
ORG_ID=os.getenv('ORG_ID')
if not RD_IP:
    print("RD_IP is not defined")
    exit()
if not TOKEN_API:
    print("TOKEN_API is not defined")
    exit()
if not ORG_ID:
    print("ORG_ID is not defined")
    exit()
headers={'Authorization':f"Token {TOKEN_API}"}
API_EP=f"/api/v1/orgs/{ORG_ID}/sites"
url = f"https://{RD_IP}{API_EP}"
with open("sites.yaml") as f1:
    d1 = f1.read()
sites = yaml.load(d1,Loader=yaml.FullLoader)
for i in sites:
    print(f"create sites {i['name']}")
    x = requests.post(url,headers=headers,json=i,verify=False)
    print(f"status {x.status_code}")
    # pprint.pprint(i)
# print(url)
# print(f"creating new site {new_site}")
# x = requests.post(url,headers=headers,json=new_site,verify=False)
# print(x)