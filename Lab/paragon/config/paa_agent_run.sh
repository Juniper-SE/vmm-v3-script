#!/bin/bash
IMAGE=localhost/paa/test-agent-application:4.4.1.16
sudo podman  run --network=host --cap-add=NET_ADMIN --device=/dev/net/tun -d \
    --privileged -v $(pwd)/config:/config -v /var/run/netns:/var/run/netns \
    --log-opt max-size=10m --log-opt max-file=2 ${IMAGE} \
    --config /config/agent.conf -A