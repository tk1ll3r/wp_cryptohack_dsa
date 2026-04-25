from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
from pwn import *
import json
from sympy.ntheory.residue_ntheory import discrete_log

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    return plaintext.decode('ascii')

def recv_json(r):
    """Đọc từng dòng cho đến khi tìm được JSON hợp lệ."""
    while True:
        line = r.recvline(timeout=15).decode(errors='ignore').strip()
        print("[<]", line)
        if not line:
            continue
        # Tìm phần JSON trong dòng (bắt đầu từ '{')
        idx = line.find('{')
        if idx != -1:
            try:
                return json.loads(line[idx:])
            except json.JSONDecodeError:
                continue

r = remote('socket.cryptohack.org', 13379)

# ---- Bước 1: Server yêu cầu gửi cho Bob ----
# Đọc đến khi gặp "Send to Bob"
r.recvuntil(b'Send to Bob:', timeout=15)
r.sendline(b'{"supported": ["DH64"]}')
print("[>] Sent: supported DH64")

# ---- Bước 2: Đọc phần Intercepted from Bob (để lấy "chosen") ----
# rồi server yêu cầu gửi cho Alice
r.recvuntil(b'Send to Alice:', timeout=15)
r.sendline(b'{"chosen": "DH64"}')
print("[>] Sent: chosen DH64")

# ---- Bước 3: Intercepted from Alice → p, g, A ----
r.recvuntil(b'Intercepted from Alice:', timeout=15)
line = r.recvline(timeout=15).decode(errors='ignore').strip()
print("[<] Alice params:", line)
data = json.loads(line)
p = int(data["p"], 16)
g = int(data["g"], 16)
A = int(data["A"], 16)
print(f"    p = {hex(p)}\n    g = {hex(g)}\n    A = {hex(A)}")

# ---- Bước 4: Intercepted from Bob → B ----
r.recvuntil(b'Intercepted from Bob:', timeout=15)
line = r.recvline(timeout=15).decode(errors='ignore').strip()
print("[<] Bob pubkey:", line)
data = json.loads(line)
B = int(data["B"], 16)
print(f"    B = {hex(B)}")

# ---- Bước 5: Intercepted from Alice → encrypted flag ----
r.recvuntil(b'Intercepted from Alice:', timeout=15)
line = r.recvline(timeout=15).decode(errors='ignore').strip()
print("[<] Encrypted flag:", line)
data = json.loads(line)
iv = data["iv"]
ciphertext = data["encrypted_flag"]

# ---- Giải discrete log (p là 64-bit, rất nhanh) ----
print("[*] Solving discrete log...")
a = discrete_log(p, A, g)
print(f"[*] a = {a}")

shared_secret = pow(B, a, p)
print(f"[*] Shared secret = {shared_secret}")
print("[+] Flag:", decrypt_flag(shared_secret, iv, ciphertext))