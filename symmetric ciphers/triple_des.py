import requests
from json import loads
from Crypto.Util.Padding import unpad

def encrypt(key, pt):
    key_hex = key.hex()
    pt_hex = pt.hex()
    url = f"https://aes.cryptohack.org/triple_des/encrypt/{key_hex}/{pt_hex}/"
    r = requests.get(url)
    ct = loads(r.text)['ciphertext']
    return bytes.fromhex(ct)

def encrypt_flag(key):
    key_hex = key.hex()
    url = f"https://aes.cryptohack.org/triple_des/encrypt_flag/{key_hex}/"
    r = requests.get(url)
    ct = loads(r.text)['ciphertext']
    return bytes.fromhex(ct)

keys = [
    b'\x00'*8 + b'\xff'*8,
    b'\xff'*8 + b'\x00'*8,
    b'\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01',
    b'\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00'
]


for key in keys:
    try:
        enc = encrypt_flag(key)
        
        flag = unpad(encrypt(key, enc), 8).decode()
        
        print(f"[+] Tìm thấy Weak Key hợp lệ: {key}")
        print(f"\n[🎉] FLAG: {flag}")
        break
    except Exception as e:
        print(f'[-] Khóa {key} không thành công.')