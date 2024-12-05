# MySQL installation

sudo apt install mariadb-server
sudo mysql_secure_installation
sudo freeradius-mysql

# Create admin user

sudo -s
mysql -u root -p 
GRANT ALL ON *.* TO 'admin'@'localhost' IDENTIFIED BY 'pass01' WITH GRANT OPTION;
FLUSH PRIVILEGES;


# create freeradius user on mysql 

CREATE DATABASE radius;
CREATE USER 'radius'@'localhost' IDENTIFIED by 'pass01';
GRANT ALL PRIVILEGES ON radius.* TO 'radius'@'localhost';
FLUSH PRIVILEGES;


# load freeradius schema into maria DB

sudo -s
cd /etc/freeradius/3.0/mods-config/sql/main/mysql
mysql -u radius -p radius < schema.sql
mysql -u radius -p radius -e "show tables"
cd /etc/freeradius/3.0/available
sudo ln -s  ../mods-available/sql ../mods-enabled/sql
sudo sed -i -e 's/dialect = "sqlite"/dialect = "mysql"/' sql 
sudo sed -i -e 's/driver = "rlm_sql_null"/driver = "rlm_sql_${dialect}"/' sql 


# modify  file /etc/freeradius/3.0/mods-enabled/sql
edit file /etc/freeradius/3.0/mods-available/sql, and change the following entry (remove the comment (#))

server = "localhost"
port = 3306
login = "radius"
password = "pass01"
radius_db = "radius"
read_clients = yes
client_table = "nas"

# change the owner of file /etc/freeradius/3.0/mods-enabled/sql

sudo chgrp -h freerad /etc/freeradius/3.0/mods-enabled/sql
sudo chown -R freerad:freerad  /etc/freeradius/3.0/mods-enabled/sql



# to configure freeradius to use mysql;
1. delete the content of clients.conf and authorize
2. Run the following command on mysql server


insert into nas (nasname,secret,shortname) values ("172.16.12.1","pass01","bng1");
insert into nas (nasname,secret,shortname) values ("172.16.12.2","pass01","bng2");
insert into nas (nasname,secret,shortname) values ("172.16.11.111","pass01","node1");
insert into nas (nasname,secret,shortname) values ("172.16.11.112","pass01","node2");
insert into nas (nasname,secret,shortname) values ("172.16.1.1","pass01","cups");

insert into radcheck (username,attribute,value,op) values ("cpe1","Cleartext-Password","pass01",":=");
insert into radcheck (username,attribute,value,op) values ("cpe1","Auth-Type","Accept",":=");
insert into radcheck (username,attribute,value,op) values ("cpe2","Cleartext-Password","pass01",":=");
insert into radcheck (username,attribute,value,op) values ("cpe2","Auth-Type","Accept",":=");
insert into radcheck (username,attribute,value,op) values ("cpe3","Cleartext-Password","pass03",":=");
insert into radcheck (username,attribute,value,op) values ("cpe3","Auth-Type","Accept",":=");
insert into radcheck (username,attribute,value,op) values ("cpe4","Cleartext-Password","pass04",":=");
insert into radcheck (username,attribute,value,op) values ("cpe4","Auth-Type","Accept",":=");




insert into radreply (username,attribute,value,op) values ("cpe1","ERX-virtual-Router-Name","isp1",":=");
insert into radreply (username,attribute,value,op) values ("cpe2","ERX-virtual-Router-Name","isp2",":=");
insert into radreply (username,attribute,value,op) values ("cpe3","ERX-virtual-Router-Name","isp3",":=");
insert into radreply (username,attribute,value,op) values ("cpe4","ERX-virtual-Router-Name","isp1",":=");

