#!/usr/bin/env python3
# to set and delete  route target, router_external status, floating ip pools and ipam

import requests, os, yaml
from vnc_api import vnc_api

template_name='fw4'
api_server_host='127.0.0.1'
vnc=vnc_api.VncApi(api_server_host=api_server_host)
template = vnc_api.ServiceTemplate(name=template_name)
properties = vnc_api.ServiceTemplateType(
    service_mode='in-network',
    service_type='firewall' ,
    version=2
)
properties.add_interface_type(
    vnc_api.ServiceTemplateInterfaceType(
        service_interface_type='left'
    )
)
properties.add_interface_type(
    vnc_api.ServiceTemplateInterfaceType(
        service_interface_type='right'
    )
)
template.set_service_template_properties(properties)
vnc.service_template_create(template)

