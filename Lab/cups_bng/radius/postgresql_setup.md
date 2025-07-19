# create admin user
    sudo -s
    su - postgres
    createuser radius --no-superuser --no-createdb --no-createrole -P
    createdb radius --owner=radius
    exit

# load the sql schema
    sudo -s
    cd /etc/freeradius/3.0/mods-config/sql/main/postgresql
    psql -U radius -h localhost radius < schema.sql
    psql -U radius -h localhost  radius < setup.sql

# load data into the database

 
    cat << EOF | tee bng_lab.sql 
    insert into nas (nasname,secret,shortname) values ('172.16.12.1','pass01','bng1');
    insert into nas (nasname,secret,shortname) values ('172.16.12.2','pass01','bng2');
    insert into nas (nasname,secret,shortname) values ('172.16.11.111','pass01','node1');
    insert into nas (nasname,secret,shortname) values ('172.16.11.112','pass01','node2');
    insert into nas (nasname,secret,shortname) values ('172.16.1.1','pass01','cups');

    insert into radcheck (username,attribute,value,op) values ('cpe1','Cleartext-Password','pass01',':=');
    insert into radcheck (username,attribute,value,op) values ('cpe1','Auth-Type','Accept',':=');
    insert into radcheck (username,attribute,value,op) values ('cpe2','Cleartext-Password','pass01',':=');
    insert into radcheck (username,attribute,value,op) values ('cpe2','Auth-Type','Accept',':=');
    insert into radcheck (username,attribute,value,op) values ('cpe3','Cleartext-Password','pass03',':=');
    insert into radcheck (username,attribute,value,op) values ('cpe3','Auth-Type','Accept',':=');
    insert into radcheck (username,attribute,value,op) values ('cpe4','Cleartext-Password','pass04',':=');
    insert into radcheck (username,attribute,value,op) values ('cpe4','Auth-Type','Accept',':=');

    insert into radcheck (username,attribute,value,op) values ('cpe1','Simultaneous-Use','1',':=');
    insert into radcheck (username,attribute,value,op) values ('cpe2','Simultaneous-Use','1',':=');
    insert into radcheck (username,attribute,value,op) values ('cpe3','Simultaneous-Use','1',':=');
    insert into radcheck (username,attribute,value,op) values ('cpe4','Simultaneous-Use','1',':=');

    insert into radreply (username,attribute,value,op) values ('cpe1','ERX-Ingress-Policy-Name','police-5M',':=');
    insert into radreply (username,attribute,value,op) values ('cpe1','ERX-Egress-Policy-Name','police-5M',':=');
    insert into radreply (username,attribute,value,op) values ('cpe1','ERX-IPv6-Ingress-Policy-Name','police-5Mv6',':=');
    insert into radreply (username,attribute,value,op) values ('cpe1','ERX-IPv6-Egress-Policy-Name','police-5Mv6',':=');


    insert into radreply (username,attribute,value,op) values ('cpe2','ERX-Ingress-Policy-Name','police-10M',':=');
    insert into radreply (username,attribute,value,op) values ('cpe2','ERX-Egress-Policy-Name','police-10M',':=');
    insert into radreply (username,attribute,value,op) values ('cpe2','ERX-IPv6-Ingress-Policy-Name','police-10Mv6',':=');
    insert into radreply (username,attribute,value,op) values ('cpe2','ERX-IPv6-Egress-Policy-Name','police-10Mv6',':=');


    insert into radreply (username,attribute,value,op) values ('cpe3','ERX-Ingress-Policy-Name','police-1M',':=');
    insert into radreply (username,attribute,value,op) values ('cpe3','ERX-Egress-Policy-Name','police-1M',':=');
    insert into radreply (username,attribute,value,op) values ('cpe3','ERX-IPv6-Ingress-Policy-Name','police-1Mv6',':=');
    insert into radreply (username,attribute,value,op) values ('cpe3','ERX-IPv6-Egress-Policy-Name','police-1Mv6',':=');

    insert into radreply (username,attribute,value,op) values ('cpe4','ERX-Ingress-Policy-Name','police-5M',':=');
    insert into radreply (username,attribute,value,op) values ('cpe4','ERX-Egress-Policy-Name','police-5M',':=');
    insert into radreply (username,attribute,value,op) values ('cpe4','ERX-IPv6-Ingress-Policy-Name','police-5Mv6',':=');
    insert into radreply (username,attribute,value,op) values ('cpe4','ERX-IPv6-Egress-Policy-Name','police-5Mv6',':=');

    insert into radreply (username,attribute,value,op) values ('cpe1','ERX-Virtual-Router-Name','isp1',':=');
    insert into radreply (username,attribute,value,op) values ('cpe2','ERX-Virtual-Router-Name','isp2',':=');
    insert into radreply (username,attribute,value,op) values ('cpe3','ERX-Virtual-Router-Name','isp3',':=');
    insert into radreply (username,attribute,value,op) values ('cpe4','ERX-Virtual-Router-Name','isp2',':=');

    EOF

    psql -U radius -h localhost radius < bng_lab.sql

# edit freeradius configuration

    cat << EOF | sudo tee /etc/freeradius/3.0/clients.conf

       client bng1 {
          ipaddr = 172.16.12.1
          secret = pass01
        }
        client bng2 {
          ipaddr = 172.16.12.2
          secret = pass01
        }
    EOF

    sudo vi /etc/freeradius/3.0/radiusd.conf

    # $INCLUDE clients.conf
    $INCLUDE mods-enabled/sql

    vi /etc/freeradius/3.0/sites-enabled/default
    vi /etc/freeradius/3.0/sites-enabled/inner-tunnel

    # files
    sql

    disable "files"
    enable "sql"

    sudo ln -s  /etc/freeradius/3.0/mods-available/sql  /etc/freeradius/3.0/mods-enabled/sql

    sudo vi  /etc/freeradius/3.0/mods-available/sql
    dialect = "postgresql"  
    read_clients = yes
    # driver = "rlm_sql_null"
    driver = "rlm_sql_${dialect}"
    # radius_db = "radius"
    radius_db = "dbname=radius host=localhost user=radius password=pass01"

# openwrt configuration

    edit /etc/config/network

    config interface wan
        option ifname 'eth1'
        option proto 'pppoe'
        option username 'cpe1'
        option password 'pass01'
        option ipv6 'auto'


