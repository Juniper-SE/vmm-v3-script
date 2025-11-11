#!/usr/bin/env python3
import requests, json, os, pprint, yaml
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
#print(headers)
print(url)
x = requests.get(url, headers=headers,verify=False)
# print(x.text)
y=json.loads(x.text)
# pprint.pprint(y)
with open("sites_id.yaml","w") as f1:
    f1.write("---\n")
    for i in y:
        # if i['name']=='PE2' or i['name']=='PE3':
        # pprint.pprint(i)
        f1.write(f"{i['name']}: {i['id']}\n")
        #sites[i['name']]=i['id']
    # print(json.loads(x.text)['cmd'])
    # with open("sites_id.yaml","w") as f1:
    #     f1.write(sites)

