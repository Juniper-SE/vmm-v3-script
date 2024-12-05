# Simple Web-Server

from flask import Flask
import subprocess
from flask import request

app = Flask(__name__)

def workers(arg1=""):
    cmd_ip = 'ifconfig | sed -n 2p | cut -d ":" -f2 | cut -d " " -f1 | tr -d "\n"'
    cmd_hostname = 'hostname | tr -d "\n"'
    visitor_ip1 = request.remote_addr
    visitor_ip2 = request.access_route[0]
    user_agent = str(request.user_agent)
    if visitor_ip1 != visitor_ip2:
        visitor_ip = "proxy : " + visitor_ip1 + ", client host : " + visitor_ip2
    else:
        visitor_ip = visitor_ip1
    hostname_header = request.headers.get('Host')
    ip_addr = str(subprocess.check_output(cmd_ip, shell=True),'utf-8')
    hostname = str(subprocess.check_output(cmd_hostname, shell=True),'utf-8')
    if 'curl' in user_agent.lower():
      retval1='''
<html><head></head><body>
User agent : ''' + user_agent + '''
this page is served by pod : ''' + hostname + ''' ## ip :''' + ip_addr + '''
client is accessing from : ''' + visitor_ip + '''
hostname access by client ''' + hostname_header
      retval2="\n</body><html>"
      if arg1=="":
        retval = retval1 + retval2 
      else:
        retval = retval1 + "\nYou are accessing : /" + arg1 + retval2
    else:
      retval1='''
        <html>
        <style>
          h1   {color:green}
          h2   {color:red}
        </style>
          <div align="center">
          <head>
            <title>Contrail Pod</title>
          </head>
          <body>
            <h1>Hello</h1><br>
            <h2>User agent = ''' + user_agent + '''</h2>
            <h2>This page is served by a <b>Contrail</b> pod</h2><br>
            <h3>IP address = ''' + ip_addr + '''<br>Hostname = ''' + hostname + '''</h3>
            <h3>You are acccessing from ''' + visitor_ip +''' </h3>
            <h3>Hostname HEADER = ''' + hostname_header + ''' </h3>
        '''
      retval2='''
          </body>
          </div>
        </html>'''
      if arg1=="":
        retval = retval1 + retval2
      else:
        retval = retval1 + "   <h3>You are accessing  /" + arg1 + "</h3>" + retval2
    return retval

@app.route('/')
def root():
    return workers()

@app.route('/<any_string>')
def contrail(any_string):
    return workers(any_string)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)

