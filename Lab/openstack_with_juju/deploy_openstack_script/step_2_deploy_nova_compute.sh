#!/bin/bash
juju deploy -n 4 --to 0,1,2,3 --channel 2023.2/stable --config nova-compute.yaml nova-compute