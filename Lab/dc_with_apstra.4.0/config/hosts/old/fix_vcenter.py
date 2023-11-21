#!/usr/bin/python

import os
import requests
import urllib3

urllib3.disable_warnings()

username = 'admin'
password = 'admin'
aos_url = 'https://172.16.10.10'

try:
    auth_resp = requests.post(
        '%s/api/aaa/login' % aos_url,
        json=dict(username=username, password=password),
        verify=False)
    assert auth_resp.ok, "Login failed: %s %s" % (auth_resp.status_code, auth_resp.json().get('errors'))
    token = auth_resp.json()['token']

    sys_resp = requests.get(
        '%s/api/systems' % aos_url,
        headers=dict(AuthToken=token),
        verify=False)
    assert sys_resp.ok, "Get systems failed: %s %s" % (sys_resp.status_code, sys_resp.json().get('error'))

    vmware = list(filter(lambda x: x['facts']['vendor'] == 'Vmware', sys_resp.json()['items']))
    assert not len(vmware) == 0, "Error: Cannot find the VMware vCenter Server in AOS."
    assert not len(vmware) > 1, "Error: Found %s VMware vCenter Server in AOS" % len(vmware)

    svc_resp = requests.put(
        '%s/api/systems/%s/services/virtual_infra' % (aos_url, vmware[0]['id']),
        headers=dict(AuthToken=token),
        json=dict(
            input='{"lldp_fetch_frequency": 1}',
            interval=30,
            name='virtual_infra',
            execution_count=-1),
        verify=False)
    assert svc_resp.ok, "Update services failed: %s %s" % (svc_resp.status_code, svc_resp.json().get('error'))
    print('Update VMware vCenter service success.')

except AssertionError as err:
    print(err.message)
