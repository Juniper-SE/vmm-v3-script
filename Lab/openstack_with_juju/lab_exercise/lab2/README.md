# Lab Exercise 2
In this lab exercise, the following will be configured
- create virtual network on contrail controller
- configure virtual network as external. 
  IP address from this virtual network will assigned as floating ip which will be advertised to the external network
- configure route target on the virtual network.
  The route target will be use to export and import routing information between SDN gateway and contrail controller

## Creating External Virtual network
1. From the web browser, open contrail command dashboard
2. from the menu, select Overlay > Virtual Network, and click Create
3. Create a virtual network with the following parameter :
    - Name : External1
    - subnet: 
        * CIDR : 172.16.1.0/28
    - Routing, Bridging and Policies:
        * Export Route target: 64512:10001
        * Import Route target : 64512:10000
    - Advanced:
        * External : yes
        * Shared: yes
4. Click Create


[Back to main page](../README.md)