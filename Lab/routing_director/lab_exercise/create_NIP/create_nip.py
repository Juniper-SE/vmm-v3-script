#!/usr/bin/env python3 
import json, yaml
from jinja2 import Template
import sys
import os


if len(sys.argv) < 2:
    print("where is the outfile name ?")
    exit(1)
outfile=sys.argv[1]
if not os.path.isfile("nodes.yaml"):
    print("file nodes.yaml is not available")
    exit(1)
if not os.path.isfile("plan.yaml"):
    print("file plan.yaml is not available")
    exit(1)
print(f"writing file {outfile}")
with open("nodes.yaml") as f1:
    data1_yaml = f1.read()
nodes=yaml.load(data1_yaml,Loader=yaml.FullLoader)
with open("plan.yaml") as f1:
    t1 = f1.read()
d0=Template(t1).render(nodes)
d1=yaml.load(d0,Loader=yaml.FullLoader)
with open(outfile,"w") as f1:
    f1.write(json.dumps(d1,indent=2))