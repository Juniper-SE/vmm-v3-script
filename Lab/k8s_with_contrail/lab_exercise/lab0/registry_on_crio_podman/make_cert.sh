mkdir -p ~/registry/certs
mkdir -p ~/registry/data
linenum=`grep -n '^\[ v3_ca'  /etc/ssl/openssl.cnf | cut -f 1 -d :`
addline="${linenum} a subjectAltName=IP:172.16.14.10"
sudo sed -i -e "${addline}" /etc/ssl/openssl.cnf
openssl req -newkey rsa:4096 -nodes -sha256 -keyout ~/registry/certs/registry.key -x509 -days 365 -out ~/registry/certs/registry.crt
