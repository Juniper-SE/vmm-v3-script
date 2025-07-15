#!/usr/bin/env python3
import subprocess
import yaml
from jinja2 import Template
import os
import json
from passlib.hash import md5_crypt


# devices=['spine1','spine2','leaf1','leaf2','leaf3','leaf4']
with open(f"topo2.yaml") as f1:
         t1 = f1.read()
p1=yaml.load(t1,Loader=yaml.FullLoader)
devices = p1.keys()
with open("underlay_bgp.j2") as f1:
    j2=f1.read()
for i in devices:
    # with open(f"{i}.yaml") as f1:
    #     t1 = f1.read()
    # p1=yaml.load(t1,Loader=yaml.FullLoader)
    conf=Template(j2).render(p1[i])
    with open(f"conf/{i}.conf","w") as f1:
        f1.write(conf)



