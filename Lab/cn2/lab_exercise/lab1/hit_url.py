#!/usr/bin/env python3
import sys
import requests
import socket

def get_url(URL):
    # proxies={'http': 'socks5://127.0.0.1:1080'}
    # r=requests.get(URL,proxies=proxies)
    r=requests.get(URL)
    s1=r.text[r.text.index('Hostname'):]
    s2=s1[:s1.index('</h3>')].replace(" ","").split('=')
	# s1=r.text[r.text.index('IP address'):]
    return s2[1]

def ip_ok(dest):
    retval = True
    if '.' not in dest:
        retval = False
    else:
        s1 = dest.split('.')
        if len(s1) != 4:
            retval = False
        else:
            for i in s1:
                if not i.isnumeric():
                    retval=False
                    break
                else:
                    if not is_ip(i):
                        retval = False
    return retval

def is_ip(num):
    retval = True
    i = int(num)
    if i < 0 or i  > 255:
       retval = False
    return retval

def run_hit(URL,number_of_try):
    list_of_ip={}
    print("Running {} times".format(number_of_try))
    print("Start")
    for i in list(range(number_of_try)):
        ip=get_url(URL)
	    # print("{} {}".format(i,ip))
        p=i % 10
        if p == 0:
            print("Step %d " %(i))
        if ip not in list_of_ip.keys():
            list_of_ip[ip]=1
        else:
            list_of_ip[ip] += 1
    print("End")
    for i in list_of_ip.keys():
        print("POD {}, number of hit {} ".format(i,list_of_ip[i]))

if len(sys.argv) == 1:
    print("where is the target and count ?")
else:
    if 'target' not in str(sys.argv):
        print("where is the target ?")
    else:
        s1=sys.argv[1:]
        c2=300
        port=80
        run_it = False
        pref=False
        for x in s1:
            if 'target' in x:
                if "=" not in x:
                    print("wrong format")
                    run_it = False
                else:
                    _,dest=x.split("=")
                    print("destination ",dest)
                    run_it = True
            if 'count' in x:
                if "=" not in x:
                    print("wrong format count")
                    run_it = False
                else:
                    _,c1=x.split("=")
                    if c1.isnumeric():
                        c2 = int(c1)
                        run_it=True
            if 'port' in x:
                if "=" not in x:
                    print("wrong format count")
                    run_it = False
                else:
                    _,c1=x.split("=")
                    if c1.isnumeric():
                        port = int(c1)
                        run_it=True
            if 'pref' in x:
                if "=" not in x:
                    print("wrong format count")
                    run_it = False
                else:
                    _,c1=x.split("=")
                    pref = c1
                    run_it=True
        if run_it:
            if pref:
                URL = 'http://' +  dest + ':' + str(port) + pref
            else:
                URL = 'http://' +  dest + ':' + str(port)
            print("URL ",URL)
            run_hit(URL,c2)




