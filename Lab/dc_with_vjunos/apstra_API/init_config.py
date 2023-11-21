#!/usr/bin/env python3
import apstra_api
import yaml
# main program

asn="""
items:
- name: ASN_Spine_DC1
  first: 65101
  last: 65109
- name: ASN_Leaf_DC1
  first: 65111
  last: 65119
- name: ASN_Collapsed_DC2
  first: 65211
  last: 65219
- name: ASN_Spine_DC3
  first: 65301
  last: 65309
- name: ASN_Leaf_DC3
  first: 65311
  last: 65319
"""
# asn="""
# items:
# - name: ASN_Spine_DC1
#   first: 65001
#   last: 65009
# - name: ASN_Leaf_DC1
#   first: 65011
#   last: 65019
# """
asn_dict = yaml.load(asn,Loader=yaml.FullLoader)
for i in asn_dict['items']:
    print(f"creating pool {i['name']}")
    apstra_api.create_asn_pools(i)

ippools="""
items:
- name: Fabric_link_DC1
  subnets:
  - network: 10.101.0.0/24
- name: Loopback_Spine_DC1
  subnets:
  - network: 10.101.1.0/24
- name: Loopback_Leaf_DC1
  subnets:
  - network: 10.101.2.0/24
- name: Loopback_VRF_DC1
  subnets:
  - network: 10.101.3.0/24
- name: Fabric_link_DC2
  subnets:
  - network: 10.102.0.0/24
- name: Loopback_Collapsed_DC2
  subnets:
  - network: 10.102.2.0/24
- name: Loopback_VRF_DC2
  subnets:
  - network: 10.102.3.0/24
- name: Fabric_link_DC3
  subnets:
  - network: 10.103.0.0/24
- name: Loopback_Spine_DC3
  subnets:
  - network: 10.103.1.0/24
- name: Loopback_Leaf_DC3
  subnets:
  - network: 10.103.2.0/24
- name: Loopback_VRF_DC3
  subnets:
  - network: 10.103.3.0/24
"""
# ippools="""
# items:
# - name: Fabric_link_DC1
#   subnets:
#   - network: 10.101.0.0/24
# - name: Loopback_Spine_DC1
#   subnets:
#   - network: 10.101.1.0/24
# - name: Loopback_Leaf_DC1
#   subnets:
#   - network: 10.101.2.0/24
# - name: Loopback_VRF_DC1
#   subnets:
#   - network: 10.101.3.0/24
# """
ippools_dict = yaml.load(ippools,Loader=yaml.FullLoader)
for i in ippools_dict['items']:
    print(f"creating ip pool {i['name']}")
    apstra_api.create_ip_pools(i)


ippools="""
items:
- name: Loopback_Spine_DC1
  subnets:
  - network: fc00:dead:beef:101::/64
- name: Loopback_Leaf_DC1
  subnets:
  - network: fc00:dead:beef:102::/64
- name: Loopback_VRF_DC1
  subnets:
  - network: fc00:dead:beef:103::/64
- name: Loopback_Collapsed_DC2
  subnets:
  - network: fc00:dead:beef:202::/64
- name: Loopback_VRF_DC2
  subnets:
  - network: fc00:dead:beef:203::/64
- name: Loopback_Spine_DC3
  subnets:
  - network: fc00:dead:beef:301::/64
- name: Loopback_Leaf_DC3
  subnets:
  - network: fc00:dead:beef:302::/64
- name: Loopback_VRF_DC3
  subnets:
  - network: fc00:dead:beef:303::/64
"""
# ippools="""
# items:
# - name: Loopback_Spine_DC1
#   subnets:
#   - network: fc00:dead:beef:101::/64
# - name: Loopback_Leaf_DC1
#   subnets:
#   - network: fc00:dead:beef:102::/64
# - name: Loopback_VRF_DC1
#   subnets:
#   - network: fc00:dead:beef:103::/64
# """
ippools_dict = yaml.load(ippools,Loader=yaml.FullLoader)
for i in ippools_dict['items']:
    print(f"creating ip pool {i['name']}")
    apstra_api.create_ipv6_pools(i)

ld="""
items:
- display_name: vEX_Spine
  panels:
  - panel_layout:
      column_count: 10
      row_count: 1
    port_groups:
    - count: 10
      roles:
      - superspine
      - unused
      - leaf
      - generic
      speed:
        unit: G
        value: 1
    port_indexing:
      order: T-B, L-R
      schema: absolute
      start_index: 1
- display_name: vEX_Leaf
  panels:
  - panel_layout:
      column_count: 10
      row_count: 1
    port_groups:
    - count: 2
      roles:
      - spine
      speed:
        unit: G
        value: 1
    - count: 8
      roles:
      - unused
      - generic
      - access
      speed:
        unit: G
        value: 1
    port_indexing:
      order: T-B, L-R
      schema: absolute
      start_index: 1
- display_name: vEX_Collapsed
  panels:
  - panel_layout:
      column_count: 10
      row_count: 1
    port_groups:
    - count: 10
      roles:
      - superspine
      - unused
      - leaf
      - generic
      - peer
      - access
      - spine
      speed:
        unit: G
        value: 1
    port_indexing:
      order: T-B, L-R
      schema: absolute
      start_index: 1
"""
# - display_name: vEVO_Spine
#   panels:
#   - panel_layout:
#       column_count: 12
#       row_count: 1
#     port_groups:
#     - count: 12
#       roles:
#       - superspine
#       - leaf
#       - generic
#       speed:
#         unit: G
#         value: 10
#     port_indexing:
#       order: T-B, L-R
#       schema: absolute
#       start_index: 1
# """

# ld_dict = yaml.load(ld,Loader=yaml.FullLoader)
# for i in ld_dict['items']:
#   apstra_api.create_logical_devices(i)
