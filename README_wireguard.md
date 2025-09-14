# Installing wireguard to access VMM lab.

1. on node **GW** install wireguard software

        sudo apt install -y wireguard

2. on your workstation, install wireguard

3. Create public and private key for node **gw**

        wg genkey | tee gw.priv | wg pubkey | tee gw.pub

4. Create public and private key for your workstation

        wg genkey | tee ws1.priv | wg pubkey | tee ws1.pub

5. Create wireguard configuration file for node **gw** and save it as /etc/wireguard/wg0.conf on node **gw**

        [Interface]
        PrivateKey=<private key of gw>
        Address=192.168.199.0/31
        ListenPort=443
        [Peer]
        PublicKey=<public key of ws1>
        AllowedIPs=192.168.199.1/32

6. On node **gw**, start the wireguard using this command 

        sudo wg-quick up wg0

7. to add wireguard service to  systemd, do the following

        sudo systemctl enable wg-quick@wg0
        sudo systemctl start wg-quick@wg0


6. Create wireguard configuration file for your workstation and save it as (for example) /etc/wireguard/wg0.conf


        [Interface]
        PrivateKey=<private key of your workstation>
        Address=192.168.199.1/31
        [Peer]
        PublicKey=<public key of node gw>
        EndPoint=<ip address of eth0 of node gw >:443
        AllowedIPs=192.168.199.0/32,172.16.255.0/24,172.16.11.0/24,172.16.10.0/24 # these are the subnet which will be accessible from your workstation

7. on your workstation, start wireguard services

        sudo wg-quick up wg0

8. Verify that host on the subnets are accessible from your workstation
