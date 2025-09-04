#!/usr/bin/env python3

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ed25519
from cryptography.hazmat.backends import default_backend
import os

def create_ssh_key(d1):
	# Generate an RSA private key
	ssh_dir = os.path.expanduser('~')  + "/.ssh/"
	ssh_key_priv_file = ssh_dir + d1['name']
	ssh_key_pub_file = ssh_dir + d1['name'] + ".pub"
	# check file existence
	key_file_not_avail = 1
	if os.path.isfile(ssh_key_priv_file) and os.path.isfile(ssh_key_pub_file):
		key_file_not_avail = 0
		print("files are available")

	if key_file_not_avail:
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
		with open(ssh_key_priv_file, "wb") as f:
			f.write(pem_private_key)
		with open(ssh_key_pub_file, "wb") as f:
			f.write(ssh_public_key)
		print("Files are created")
	else:
		print("files are not created")
			

# main function
d={'name' :'lab1'}
create_ssh_key(d)
