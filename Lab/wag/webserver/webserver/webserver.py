# Simple Web-Server

from flask import Flask
import subprocess
from flask import request
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'radius'
app.config['MYSQL_DATABASE_PASSWORD'] = 'radpass'
app.config['MYSQL_DATABASE_DB'] = 'radius'
 
mysql = MySQL(app)


def workers(arg1=""):
  #cmd_ip = 'ifconfig | sed -n 2p | cut -d ":" -f2 | cut -d " " -f1 | tr -d "\n"'
  #cmd_hostname = 'hostname | tr -d "\n"'
  visitor_ip1 = request.remote_addr
  visitor_ip2 = request.access_route[0]
  user_agent = str(request.user_agent)
  if visitor_ip1 != visitor_ip2:
      visitor_ip = "proxy : " + visitor_ip1 + ", client host : " + visitor_ip2
  else:
      visitor_ip = visitor_ip1
  hostname_header = request.headers.get('Host')
  #ip_addr = str(subprocess.check_output(cmd_ip, shell=True),'utf-8')
  #hostname = str(subprocess.check_output(cmd_hostname, shell=True),'utf-8')
  # check username 
  conn = mysql.connect()
  cursor =conn.cursor()
  cmd1 = "select username, acctsessionid, nasipaddress from radacct where framedipaddress='{}' and acctstoptime is NULL".format(visitor_ip)
  cursor.execute(cmd1)
  tmp1 = cursor.fetchone()
  if tmp1:
    username = tmp1[0]
    acctsessionid = tmp1[1]
    nasipaddress= tmp1[2]
  else:
    username = ""
    acctsessionid = ""
    nasipaddress= ""
  # Check login status
  # cmd1 =  "select * from radcheck where username='{}' ".format(username)
  # cursor.execute(cmd1)
  # tmp1=cursor.fetchone()
  # logged_in = True if tmp1 else False
  # cursor.close()
  retval1=f'''
    <html><head></head><body>
    <h3>User agent : {user_agent}</h3>
    <h3>client is accessing from : {visitor_ip}</h3>
    <h3>username : {username}</h3>
    <h3>Acct Session ID : {acctsessionid}</h3>
    <h3>connected through BNG: {nasipaddress}</h3>
    <h3>hostname access by client {hostname_header}</h3>
    <a href="http://172.16.13.11/login">Click here to login</a>
    '''
  # if logged_in:
  #   retval3 = "You are logged IN<br>"
  # else:
  #   retval3 = "You are NOT logged IN<br>"
  retval2="\n</body><html>"
  retval = retval1 + retval2 if arg1 else retval1  + "\nYou are accessing : /" + arg1 + retval2
  # if arg1=="":
  #   retval = retval1 + retval2 
  # else:
  #   retval = retval1 + "\nYou are accessing : /" + arg1 + retval2
  return retval


def login1():
  visitor_ip1 = request.remote_addr
  visitor_ip2 = request.access_route[0]
  user_agent = str(request.user_agent)
  if visitor_ip1 != visitor_ip2:
      visitor_ip = "proxy : " + visitor_ip1 + ", client host : " + visitor_ip2
  else:
      visitor_ip = visitor_ip1
  conn = mysql.connect()
  cursor =conn.cursor()
  cmd1 = "select username, acctsessionid, nasipaddress, acctuniqueid from radacct where framedipaddress='{}' and acctstoptime is NULL".format(visitor_ip)
  cursor.execute(cmd1)
  tmp1 = cursor.fetchone()
  if tmp1:
    username = tmp1[0]
    acctsessionid = tmp1[1]
    nasipaddress= tmp1[2]
    acctuniqueid=tmp1[3]
    filename1 = f"/tmp/{acctuniqueid}.coa"
    with open(filename1,'w') as f1:
      f1.write(f"User-Name=\"{username}\"\n")
      f1.write(f"Acct-Session-Id={acctsessionid }\n")
      f1.write(f"ERX-Service-Deactivate:1=\"redirDynamic\"\n")
    cmd_coa=f"radclient -f {filename1} {nasipaddress} coa jnpr123"
    result_coa=str(subprocess.check_output(cmd_coa, shell=True),'utf-8')
    retval1=f'''
      <html><head></head><body>
      <h3>username {username} is allowed to access now<h3>
      <h3> Coa Result </h3>
      result {result_coa}<br>
      <a href="https://www.google.com">Google.com</a>
    '''
    retval2="\n</body><html>"
    retval = retval1 + retval2
  else:
    retval =""
  return retval

def logout1():
  visitor_ip1 = request.remote_addr
  visitor_ip2 = request.access_route[0]
  user_agent = str(request.user_agent)
  if visitor_ip1 != visitor_ip2:
      visitor_ip = "proxy : " + visitor_ip1 + ", client host : " + visitor_ip2
  else:
      visitor_ip = visitor_ip1
  conn = mysql.connect()
  cursor =conn.cursor()
  cmd1 = "select username, acctsessionid, nasipaddress, acctuniqueid from radacct where framedipaddress='{}' and acctstoptime is NULL".format(visitor_ip)
  cursor.execute(cmd1)
  tmp1 = cursor.fetchone()
  if tmp1:
    username = tmp1[0]
    acctsessionid = tmp1[1]
    nasipaddress= tmp1[2]
    acctuniqueid=tmp1[3]
    filename1 = f"/tmp/{acctuniqueid}.coa"
    with open(filename1,'w') as f1:
      f1.write(f"User-Name=\"{username}\"\n")
      f1.write(f"Acct-Session-Id={acctsessionid }\n")
      f1.write(f"ERX-Service-Activate:1 += \"redirDynamic(http://172.16.13.11)\"\n")
    cmd_coa=f"radclient -f {filename1} {nasipaddress} coa jnpr123"
    result_coa=str(subprocess.check_output(cmd_coa, shell=True),'utf-8')
    retval1=f'''
      <html><head></head><body>
      <h3>username {username} is logout now<h3>
      <h3> Coa Result </h3>
      result {result_coa}<br>
      <a href="https://www.google.com">Google.com</a>
    '''
    retval2="\n</body><html>"
    retval = retval1 + retval2
  else:
    retval =""
  return retval

@app.route('/')
def root():
    return workers()
  
@app.route('/login')
def login():
    return login1()

@app.route('/logout')
def logout():
    return logout1()

@app.route('/<any_string>')
def contrail(any_string):
    return workers(any_string)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)

