#!/usr/bin/env python3
import requests, json, os
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
API_EP=f"/api/v1/orgs/{ORG_ID}/ocdevices/outbound_ssh_cmd"
url = f"https://{RD_IP}{API_EP}"
x = requests.get(url, headers=headers,verify=False)
with open("../ansible/onboarding.set","w") as f1:
    print(json.loads(x.text)['cmd'])
    f1.write(json.loads(x.text)['cmd'])