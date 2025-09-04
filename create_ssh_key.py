#!/usr/bin/env python3
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ed25519
from cryptography.hazmat.backends import default_backend

# Generate an RSA private key
rsa_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Serialize the RSA private key to OpenSSH format
pem_private_key = rsa_private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.OpenSSH,
    encryption_algorithm=serialization.NoEncryption() # Use NoEncryption or a password
)

# Get the public key in OpenSSH format
ssh_public_key = rsa_private_key.public_key().public_bytes(
    encoding=serialization.Encoding.OpenSSH,
    format=serialization.PublicFormat.OpenSSH
)

# Save to files
with open("/Users/irzan/.ssh/id_rsa_cryptography", "wb") as f:
    f.write(pem_private_key)
with open("/Users/irzan/.ssh/id_rsa_cryptography.pub", "wb") as f:
    f.write(ssh_public_key)
