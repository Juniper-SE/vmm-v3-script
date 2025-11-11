#!/usr/bin/env python3
import requests, os, json

RD_IP=os.getenv('RD_IP')
RD_USER=os.getenv('RD_USER')
RD_PASSWD=os.getenv('RD_PASSWD')
TOKEN_ID=os.getenv('TOKEN_ID')
if not RD_IP:
    print("RD_IP is not defined")
    exit()
if not RD_USER:
    print("RD_USER is not defined")
    exit()
if not RD_PASSWD:
    print("RD_PASSWD is not defined")
    exit()
if not TOKEN_ID:
    print("TOKEN_ID is not defined")
    exit()
auth_id=(RD_USER,RD_PASSWD)
# if not ORG_ID:
#     print("ORG_ID is not defined")
#     exit()
# login_id={"email" : RD_USER,"password":RD_PASSWD}
# API_EP="/api/v1/login"
# API_EP="/api/v1/orgs/stats"
API_EP=f"/api/v1/self/apitokens/{TOKEN_ID}"
url = f"https://{RD_IP}{API_EP}"
print(f"URL {url}")
print(f"deleting token {TOKEN_ID}")
# print(f" LOGIN ID {login_id}")
# x = requests.post(url, json = login_id,verify=False)
# x = requests.get(url,auth=(RD_USER,RD_PASSWD),verify=False)
# x = requests.post(url,auth=(RD_USER,RD_PASSWD),verify=False)
x=requests.delete(url,auth=auth_id,verify=False)
print(x)
# result = json.loads(x.text)
# print(result)
