#!/usr/bin/env python3
# to set and delete  route target, router_external status, floating ip pools and ipam

import requests, os, yaml
from vnc_api import vnc_api
host='127.0.0.1'
proj_name='k8s-ns3'
vnc=vnc_api.VncApi(api_server_host=host)
project_list=vnc.projects_list()
print(project_list)
project = vnc.project_read(fq_name=["default-domain",proj_name])
print(project)
vnc.project_delete(project)