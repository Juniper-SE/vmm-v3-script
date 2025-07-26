apk add apache2 php-apache2


cat << EOF | tee /var/www/localhost/htdocs/index.html
<html>
<body>
<h1>This is Web1</h1>
<h1>it works </h1>
Welcome to server web1.vmmlab.com<p>
This is just a test inside the lab<p>
please don't be afraid <p>
</body>
</html>
EOF

cat << EOF | tee /var/www/localhost/htdocs/index.php
cat << EOF | tee ./index.php
<?php
echo '<html>';
echo '<head>This is the page</head>';
echo '<body>';
echo '<h1>Welcome</h1>';
echo 'Server name '.\$_SERVER['HTTP_HOST'];
echo '<p>';
echo 'IP address of the server '.\$_SERVER['SERVER_ADDR'];
echo '<p>';
echo 'you are accessing this server from '.\$_SERVER['REMOTE_ADDR'];
echo '<p>thank you ';
echo '</body></html>';
?>
EOF

cat << EOF | tee -a /etc/apache2/httpd.conf
ServerName web1.vmmlab.com
DirectoryIndex index.php index.html
EOF


sed -i -e "s/web1/web3/"  /var/www/localhost/htdocs/index.html
sed -i -e "s/web1/web3/"  /etc/apache2/httpd.conf
sed -i -e "s/101/103/" /etc/network/interfaces

service apache2 start
rc-update add apache2




 links -address-preference 2 http://web1.vmmlab.com/index.php

 sysctl -w net.ipv6.conf.eth0.disable_ipv6=0
 sysctl -w net.ipv6.conf.all.disable_ipv6=0