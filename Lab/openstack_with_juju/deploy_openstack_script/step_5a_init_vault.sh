#!/bin/bash
export VAULT_ADDR="http://172.16.11.164:8200"
vault operator init -key-shares=5 -key-threshold=3
