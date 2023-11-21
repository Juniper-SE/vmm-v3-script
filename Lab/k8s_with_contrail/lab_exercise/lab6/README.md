# configuring gateway-less forwarding
In this lab exercise, gateway-less forwarding is configured.
Gateway-less forwarding on contrail networking allow access into virtual networks inside the kubernetes cluster without using overlay tunnel, which means SDN GAteway is not required.
traffic from external network is routed directly to the worker node where the pods are running


## caveat

if there are multiple backend pods inside the kubernetes cluster, which runs on multiple worker node, then only one next-hop will be advertised to external router  if gateway-less forwarding is used.
if SDN Gateway or overlay tunnel is used, and if there are multiple backend pods inside the kubernetes cluster, which runs on multiple worker node, then multiple next-hop will be advertised by contrail controller to the SDN gateway.

