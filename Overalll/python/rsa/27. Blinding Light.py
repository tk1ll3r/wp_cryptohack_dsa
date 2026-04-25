from pwn import *
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes

io = remote('socket.cryptohack.org', 13376, level='error')

def json_send(hsh):
    io.sendline(json.dumps(hsh).encode())

def json_recv():
    return json.loads(io.recvline())

io.recvline()

json_send({"option": "get_pubkey"})
N = int(json_recv()['N'], 16)

p1 = 211578328037
p2 = 2173767566209

json_send({"option": "sign", "msg": long_to_bytes(p1).hex()})
s1 = int(json_recv()['signature'], 16)

json_send({"option": "sign", "msg": long_to_bytes(p2).hex()})
s2 = int(json_recv()['signature'], 16)

admin_signature = (s1 * s2) % N

json_send({
    "option": "verify",
    "msg": b"admin=True".hex(),

    "signature": hex(admin_signature)
})

print(f"{json_recv()['response']}")
