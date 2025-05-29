#!/usr/bin/env python3
import requests
import json
pa_ip='172.16.12.1'
email="irzan@juniper.net"
password="J4k4rt4#170845"
login_id=(email,password)
org_id='947375fa-d00b-4c57-a3b5-4ef1a197cffb'
url = f"https://{pa_ip}/api/v1/orgs/{org_id}/sites"
new_site={
        'name': 'TestSite',
        'timezone': 'Asia/Jakarta',
        'country_code': 'ID',
        'latlng': {
            'lat': 3.568395,
            'lng': 98.701615
        },
        'address': 'HP92+9JM, Jl. HM. Joni, Teladan Tim., Kec. Medan Kota, Kota Medan, Sumatera Utara, Indonesia'
    }
print(f"Creating site {new_site['name']}")
r=requests.post(url,verify=False,auth=login_id,json=new_site)
print(f"status {r.status_code}")
d1=json.load(r.content)
print(f"content {d1}")
print(f"id : {d1['id']}")

