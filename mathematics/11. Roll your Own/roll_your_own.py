from pwn import remote
from json import loads, dumps

import logging
logging.getLogger("pwnlib").setLevel(logging.ERROR)

HOST = 'socket.cryptohack.org'
PORT = 13403

def solve():
    r = remote(HOST, PORT)

    r.recvuntil(b"Prime generated: ")
    q_str = r.recvline().decode().strip()
    q = int(q_str.replace('"', ''), 16)

    g = q + 1
    n = q ** 2
    
    payload_params = {
        "g": hex(g),
        "n": hex(n)
    }

    r.recvuntil(b"Send integers (g,n) such that pow(g,q,n) = 1: ")
    r.sendline(dumps(payload_params).encode())
    r.recvuntil(b"Generated my public key: ")
    h_str = r.recvline().decode().strip()
    h = int(h_str.replace('"', ''), 16)
    x = (h - 1) // q
    payload_secret = {
        "x": hex(x)
    }
    r.recvuntil(b"What is my private key: ")
    r.sendline(dumps(payload_secret).encode())

    response = r.recvline().decode().strip()
    try:
        flag = loads(response)['flag']
        print(f"{flag}")
    r.close()

if __name__ == '__main__':
    solve()