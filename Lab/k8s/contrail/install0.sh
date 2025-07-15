yum -y install epel-release git net-tools sshpass
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
chmod +x ./get-pip.py
./get-pip.py
pip install ansible==2.7.18 PyYAML requests
