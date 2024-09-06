#!/bin/bash
AGENTNAME=mdn1agent1
PAHOST=172.16.11.22
ORGUUID=68029dd1-a28f-4035-9318-09a2e4f3cbaa
EMAIL=irzan@juniper.net
PASSWD=J4k4rt4#170845
IMAGE=localhost/paa/test-agent-application:4.4.1.16
mkdir config
sudo podman  run --rm -v $(pwd)/config:/config \
    -v  /var/run/netns:/var/run/netns \
    ${IMAGE} \
    register --config /config/agent.conf -A\
    	-s -H ${PAHOST} \
    	--org ${ORGUUID} \
    	--email ${EMAIL} \
    	--password ${PASSWD} \
    	--name ${AGENTNAME}
