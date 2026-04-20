import requests
from pwn import xor

BASE = "https://aes.cryptohack.org"

def encrypt_flag():
    r = requests.get(f"{BASE}/ecbcbcwtf/encrypt_flag/")
    return r.json()["ciphertext"]

def ecb_decrypt(block_hex):
    r = requests.get(f"{BASE}/ecbcbcwtf/decrypt/{block_hex}/")
    return bytes.fromhex(r.json()["plaintext"])

ciphertext_hex = encrypt_flag()
iv = bytes.fromhex(ciphertext_hex[:32])
c1 = bytes.fromhex(ciphertext_hex[32:64])
c2 = bytes.fromhex(ciphertext_hex[64:])

d1 = ecb_decrypt(ciphertext_hex[32:64])
d2 = ecb_decrypt(ciphertext_hex[64:])

p1 = xor(d1, iv)
p2 = xor(d2, c1)

print((p1 + p2).decode())