#!/usr/bin/env python3
import requests
import json
pa_ip='172.16.12.1'
email="irzan@juniper.net"
password="J4k4rt4#170845"
login_id=(email,password)
org_id='94fdbf5a-222a-43f2-837c-c79418e4fc12'
url = f"https://{pa_ip}/api/v1/orgs/{org_id}/sites"
new_site=[
    {
        'name': 'pe1',
        'timezone': 'Asia/Jakarta',
        'country_code': 'ID',
        'latlng': {
            'lat': 3.568395,
            'lng': 98.701615
        },
        'address': 'HP92+9JM, Jl. HM. Joni, Teladan Tim., Kec. Medan Kota, Kota Medan, Sumatera Utara, Indonesia'
    }, 
    {
        'name': 'pe2',
        'timezone': 'Asia/Jakarta',
        'country_code': 'ID',
        'latlng': {
            'lat': -2.977444, 
            'lng': 104.748514
        },
        'address': '2PFX+299, Jl. Kapten Anwar Sastro, Sungai Pangeran, Kec. Ilir Tim. I, Kota Palembang, Sumatera Selatan 30127'
    }, 
    {
        'name': 'pe3',
        'timezone': 'Asia/Jayapura',
        'country_code': 'ID',
        'latlng': {
            'lat': -3.702669, 
            'lng': 128.173830
        },
        'address': 'Jl Dr. Sitanala No.9, Kel Wainitu, Nusaniwe, Kota Ambon, Maluku'
    }, 
    {
        'name': 'pe4',
        'timezone': 'Asia/Makassar',
        'country_code': 'ID',
        'latlng': {
            'lat': -8.582092,  
            'lng': 116.097611
        },
        'address': 'C39X+336, Dasan Agung Baru, Selaparang, Mataram City, West Nusa Tenggara 83125'
    }, 
    {
        'name': 'p1',
        'timezone': 'Asia/Jakarta',
        'country_code': 'ID',
        'latlng': {
            'lat': 1.115560,   
            'lng': 104.050654
        },
        'address': '4382+47F, Baloi Permai, Batam Kota, Batam City, Riau Islands 29432'
    }, 
    {
        'name': 'p2',
        'timezone': 'Asia/Jakarta',
        'country_code': 'ID',
        'latlng': {
            'lat': -6.220706,   
            'lng': 106.873861
        },
        'address': 'QVHF+JG Rawa Bunga, East Jakarta City, Jakarta'
    }, 
    {
        'name': 'p3',
        'timezone': 'Asia/Makassar',
        'country_code': 'ID',
        'latlng': {
            'lat': -5.162501, 
            'lng': 119.433842
        },
        'address': 'Jl. A. P. Pettarani No.4, Gn. Sari, Kec. Rappocini, Kota Makassar, Sulawesi Selatan 90221'
    }, 
    {
        'name': 'p4',
        'timezone': 'Asia/Jakarta',
        'country_code': 'ID',
        'latlng': {
            'lat': -7.311704, 
            'lng': 112.728046
        },
        'address': 'MPQH+66P, Unnamed Road, Ketintang, Kec. Gayungan, Surabaya, Jawa Timur 60231'
    }, 
    {
        'name': 'p5',
        'timezone': 'Asia/Jakarta',
        'country_code': 'ID',
        'latlng': {
            'lat': -7.786667, 
            'lng': 110.374960
        },
        'address': 'Jl. Yos Sudarso No.9 001, Kotabaru, Kec. Gondokusuman, Kota Yogyakarta, Daerah Istimewa Yogyakarta 55224'
    }
]
for i in new_site:
    print(f"Creating site {i['name']}")
    r=requests.post(url,verify=False,auth=login_id,json=i)
    print(f"status {r.status_code}")
    print(f"content {r.content}")
