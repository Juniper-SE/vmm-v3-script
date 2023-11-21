#!/usr/bin/env python3
import apstra_api
import yaml
# main program

asn="""
items:
- name: ASN_DC1_Spine
  first: 65001
  last: 65009
- name: ASN_DC1_Leaf
  first: 65011
  last: 65019
- name: ASN_DC2_Collapsed
  first: 65021
  last: 65029
- name: ASN_DC3_Spine
  first: 65031
  last: 65039
- name: ASN_DC3_Leaf
  first: 65041
  last: 65049
"""
asn_dict = yaml.load(asn,Loader=yaml.FullLoader)
for i in asn_dict['items']:
    print(f"creating pool {i['name']}")
    apstra_api.create_asn_pools(i)