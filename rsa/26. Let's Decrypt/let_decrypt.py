from pwn import *
import json
from Crypto.Util.number import bytes_to_long
from pkcs1 import emsa_pkcs1_v15

io = remote("socket.cryptohack.org", 13391, level='error')

def json_send(hsh):
    io.sendline(json.dumps(hsh).encode())

def json_recv():
    return json.loads(io.recvline().decode())

io.recvline()

json_send({"option": "get_signature"})
data = json_recv()
sig = int(data["signature"], 16)

msg = "I am Mallory own CryptoHack.org"
digest = emsa_pkcs1_v15.encode(msg.encode(), 256)
digest_int = bytes_to_long(digest)

e = 1
n = sig - digest_int

json_send({
    "option": "verify",
    "msg": msg,
    "N": hex(n),
    "e": hex(e)
})

print(f"{json_recv()}")