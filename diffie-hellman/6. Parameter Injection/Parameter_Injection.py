import json
import hashlib
import re
from pwn import remote
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def json_recv(conn):
    while True:
        line = conn.recvline().strip().decode(errors='replace')
        if not line:
            continue
        match = re.search(r'\{.*\}', line)
        if match:
            return json.loads(match.group())

def json_send(conn, data):
    conn.sendline(json.dumps(data).encode())

def derive_key(shared_secret: int) -> bytes:
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    return sha1.digest()[:16]

def is_pkcs7_padded(message: bytes) -> bool:
    # Kiểm tra padding đúng cách như server
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str) -> str:
    key = derive_key(shared_secret)
    ct = bytes.fromhex(ciphertext)
    iv_bytes = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    plaintext = cipher.decrypt(ct)
    # Dùng is_pkcs7_padded như server, không dùng unpad thẳng
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    return plaintext.decode('ascii')

conn = remote("socket.cryptohack.org", 13371)

# Bước 1: Nhận {p, g, A} từ Alice
alice_msg = json_recv(conn)
p = int(alice_msg["p"], 16)

# Bước 2: Inject A = 1 → gửi cho Bob
# Bob tính: S = A^b mod p = 1^b mod p = 1
json_send(conn, {"p": hex(p), "g": alice_msg["g"], "A": hex(1)})

# Bước 3: Nhận B từ Bob → gửi B = 1 cho Alice
# Alice tính: S = B^a mod p = 1^a mod p = 1
bob_msg = json_recv(conn)
print(f"B = {bob_msg['B']}")
json_send(conn, {"B": hex(1)})

# Bước 4: Nhận iv + encrypted_flag từ Alice
cipher_msg = json_recv(conn)
print(f"Cipher -> {cipher_msg}")

# Bước 5: Decrypt với shared_secret = 1
result = decrypt_flag(1, cipher_msg["iv"], cipher_msg["encrypted_flag"])
print(f"\nFLAG: {result}")

conn.close()