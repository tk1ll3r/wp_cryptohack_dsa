from pwn import *
from json import loads, dumps
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

r = remote('socket.cryptohack.org', 13373, level='error')

def send(msg):
    r.sendline(dumps(msg).encode())

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Tạo khóa AES 16-byte từ mã băm SHA1 của shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    
    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    plaintext = cipher.decrypt(bytes.fromhex(ciphertext))
    return unpad(plaintext, 16).decode('ascii')


r.recvuntil(b'Intercepted from Alice: ')
alice_params = loads(r.recvline().decode())
p = alice_params['p']
A = alice_params['A'] 

r.recvuntil(b'Intercepted from Alice: ')
alice_msg = loads(r.recvline().decode())
iv_A = alice_msg['iv']
encrypted_A = alice_msg['encrypted']

r.recvuntil(b'Bob connects to you, send him some parameters: ')
fake_params = {
    'p': p,
    'g': A,       
    'A': '0x0'    
}
send(fake_params)

r.recvuntil(b'Bob says to you: ')
bob_response = loads(r.recvline().decode())
fake_B = bob_response['B']

# Do g' = A, nên B = (g')^b mod p = A^b mod p = Shared Secret
shared_secret = int(fake_B, 16)

flag = decrypt_flag(shared_secret, iv_A, encrypted_A)
print(f"{flag}")