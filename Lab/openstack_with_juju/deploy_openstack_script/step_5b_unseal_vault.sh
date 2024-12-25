#!/bin/bash
export VAULT_ADDR="http://172.16.11.164:8200"
export KEY1=
export KEY2=
export KEY3=
export INITIAL_TOKEN=
vault operator unseal ${KEY1}
vault operator unseal ${KEY2}
vault operator unseal ${KEY3}
export VAULT_TOKEN=${INITIAL_TOKEN}
vault token create -ttl=10m