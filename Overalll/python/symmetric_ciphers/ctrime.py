import requests
from json import loads
import string

def encrypt(pt_bytes):
    pt_hex = pt_bytes.hex()
    url = f'https://aes.cryptohack.org/ctrime/encrypt/{pt_hex}/'
    r = requests.get(url)
    ct = loads(r.text)['ciphertext']
    return len(ct) 

FLAG = b'crypto{'
chars = string.ascii_letters + string.digits + '_}'

print("[*] Đang bắt đầu Brute-force CRIME attack...")

while True:
    min_len = 9999
    best_char = ''
    
    for char in chars:
        guess = FLAG + char.encode()
        pt = guess * 2 
        
        ct_len = encrypt(pt)
        
        if ct_len < min_len:
            min_len = ct_len
            best_char = char
    FLAG += best_char.encode()
    print(f"{FLAG.decode()}")
    
    if best_char == '}':
        break