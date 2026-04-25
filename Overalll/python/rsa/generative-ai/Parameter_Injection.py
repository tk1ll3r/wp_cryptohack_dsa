#!/usr/bin/env python3
import socket
import json
import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import bytes_to_long

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    try:
        return unpad(plaintext, 16).decode('ascii')
    except:
        return plaintext.decode('ascii')

def recv_until(s, token: bytes):
    """token phải là bytes, KHÔNG gọi .encode()"""
    data = b""
    while not data.endswith(token):
        data += s.recv(1)
    return data

def recvline_json(s):
    data = b""
    while True:
        byte = s.recv(1)
        data += byte
        if byte == b"\n":
            break
    line = data.decode().strip()
    print(f"[RECV] {line}")
    return json.loads(line)

def send_json(s, obj):
    msg = json.dumps(obj) + "\n"
    print(f"[SEND] {msg.strip()}")
    s.sendall(msg.encode())

def solve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('socket.cryptohack.org', 13371))
    s.settimeout(30)
    print("[*] Connected!")

    recv_until(s, b"Intercepted from Alice: ")
    alice_msg = recvline_json(s)

    p = int(alice_msg['p'], 16)
    g = int(alice_msg['g'], 16)
    A = int(alice_msg['A'], 16)
    print(f"[*] p bits={p.bit_length()}, g={g}")

    c = bytes_to_long(os.urandom(32))

    recv_until(s, b"Send to Bob: ")
    send_json(s, {"p": hex(p), "g": hex(g), "A": hex(p)})

    recv_until(s, b"Intercepted from Bob: ")
    bob_msg = recvline_json(s)

    recv_until(s, b"Send to Alice: ")
    C = pow(g, c, p)
    send_json(s, {"B": hex(C)})

    recv_until(s, b"Intercepted from Alice: ")
    enc_msg = recvline_json(s)

    shared_secret = pow(A, c, p)
    print(f"[*] shared_secret[:32] = {hex(shared_secret)[:34]}...")

    flag = decrypt_flag(shared_secret, enc_msg['iv'], enc_msg['encrypted_flag'])
    print(f"\n✅ FLAG: {flag}")
    s.close()

solve()