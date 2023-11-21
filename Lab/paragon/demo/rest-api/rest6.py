import requests
import pprint
import json

paragon_svr='172.16.11.50'
username='admin'
password='^J4k4rt4#010507$'
header1={"Content-Type": "application/json"}
url='https://' + paragon_svr + '/iam/authenticate'
data1={ 
    'user' : {
        'domain' :'spdomain',
        'name' : 'admin'
    },
    'methods' : ['PASSWORD']
}
data1['password'] = password
d1 = json.dumps(data1).encode('utf-8')


#print(d1)
#data1.encode("utf-8")
#pprint.pprint(data1)
#print(header1)
#print(url)

r = requests.post(url,headers=header1,data=d1,auth=(username,password),verify=False)
r_json = r.json()
if r.status_code==200 and r_json['status'] == 'AUTHENTICATED':
    # print(r_json['access_token'])
    access_token = r_json['access_token']
    url = 'https://'+ paragon_svr + '/traffic-engineering/api/topology/v2/1/te-lsps'
    data1={}
    d1 = json.dumps(data1).encode('utf-8')
    header1={"Content-Type": "application/json",'x-iam-token': access_token}
    # r = requests.get(url,headers=header1,data=d1,verify=False)
    r = requests.get(url,headers=header1,verify=False)
    r_json=r.json()
    print(r.status_code)
    pprint.pprint(r_json[0])
    # pprint.pprint(r_json[0])
    # pprint.pprint(r_json)
    # print(r_json['nodes'])
    # pprint.pprint(r_json['nodes'])
    # pprint.pprint(r_json['links'][0])
    # print(r.text)
