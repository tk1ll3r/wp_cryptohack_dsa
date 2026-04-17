import requests
from json import loads

def encrypt(plaintext: bytes, iv: bytes):
    url = f'https://aes.cryptohack.org/symmetry/encrypt/{plaintext.hex()}/{iv.hex()}/'
    r = requests.get(url)
    return loads(r.text)['ciphertext']

def encrypt_flag():
    url = f'https://aes.cryptohack.org/symmetry/encrypt_flag/'
    r = requests.get(url)
    enc = bytes.fromhex(loads(r.text)['ciphertext'])
    return enc[:16], enc[16:]

iv, ct = encrypt_flag()


decrypted_hex = encrypt(ct, iv)

flag = bytes.fromhex(decrypted_hex).decode('ascii')
print(f"{flag}")