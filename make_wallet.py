from eth_keys import keys
from eth_utils import keccak
import os

# Step 1: Generate a random 32-byte private key
private_key_bytes = os.urandom(32)
private_key = keys.PrivateKey(private_key_bytes)
print(f"Private Key: {private_key}")

# Step 2: Derive the public key
public_key = private_key.public_key
print(f"Public Key: {public_key}")

# Step 3: Generate the Ethereum address
address = public_key.to_checksum_address()
print(f"Ethereum Address: {address}")
