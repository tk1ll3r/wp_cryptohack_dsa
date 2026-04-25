import hashlib
from Crypto.PublicKey import RSA

# Read the PEM file
with open('transparency.pem', 'r') as f:
    pem = f.read()

key = RSA.import_key(pem)

# Export to DER format for a consistent hash
der = key.export_key(format='DER')
sha256_hash = hashlib.sha256(der).hexdigest()

# Fixed the print syntax here:
print(f"Public Key SHA256: {sha256_hash}")