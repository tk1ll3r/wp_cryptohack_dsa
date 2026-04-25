from hashlib import sha256
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_dir, "private.key")

with open(key_path, "rb") as f:
    key_data = f.read()

key_text = key_data.decode("utf-8")
values = {}
for line in key_text.splitlines():
    name, value = line.split("=", 1)
    values[name.strip()] = int(value.strip())

N = values["N"]
d = values["d"]

message = b"crypto{Immut4ble_m3ssag1ng}"
H = bytes_to_long(sha256(message).digest())

S = pow(H, d, N)
print(S)
