#!/usr/bin/env python3
import json
import pprint
site_data_file = 'site_data.json'
source_nip_file = 'brownfield_with_NIP_1/plan.lab1_brownfield.json'
sernum_file = 'sernum.json'
new_nip_file='plan.lab1.json'
print(f"reading site_data")
with open(site_data_file) as f1:
    site_data=json.load(f1)
print(f"reading source_nip_file")
with open(source_nip_file) as f1:
    nip = json.load(f1)
print(f"reading sernum_fie")
with open(sernum_file) as f1:
    sernum = json.load(f1)

nodes = nip['infrastructure_ntw']['network_nodes']['network_node']
#pprint.pprint(nip)
new_nodes = []
for i in nodes:
    node_name = i['name']
    new_node = i
    new_node['serial']=sernum[node_name]
    new_node['site_id']=site_data[node_name]
    new_nodes.append(new_node)
nip['infrastructure_ntw']['network_nodes']['network_node'] = new_nodes
#pprint.pprint(nip)
print(f"write new nip file {new_nip_file}")
with open(new_nip_file,"w") as f1:
    json_objects = json.dumps(nip,indent=4)
    f1.write(json_objects)
    