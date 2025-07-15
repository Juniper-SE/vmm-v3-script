#!/usr/bin/env python3 
from jinja2 import Template
import yaml

with open('config_rr.j2') as f:
    template_path = f.read()
print(template_path)

with open('data1.yaml') as f:
    d1=yaml.load(f,Loader=yaml.FullLoader)

print(d1)

t1 = Template(template_path)
c1 = t1.render(d1)
print(c1)