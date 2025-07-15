#!/bin/bash
# juju deploy --to lxd:2 --channel 3.9/stable rabbitmq-server
juju deploy --to 13 --channel 3.9/stable rabbitmq-server
juju integrate rabbitmq-server:amqp neutron-api:amqp
juju integrate rabbitmq-server:amqp nova-compute:amqp
