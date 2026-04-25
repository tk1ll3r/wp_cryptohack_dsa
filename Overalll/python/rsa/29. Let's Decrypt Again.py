from pwn import *
from json import dumps, loads
from Crypto.Util.number import bytes_to_long
from pkcs1 import emsa_pkcs1_v15
from sage.all import Mod, discrete_log

r = remote('socket.cryptohack.org', 13394)
r.recvline()

r.sendline(dumps({'option': 'get_signature'}).encode())
s = int(loads(r.recvline())['signature'], 16)

p, k = 2010103, 50
n = p**k
r.sendline(dumps({'option': 'set_pubkey', 'pubkey': hex(n)}).encode())
suffix = loads(r.recvline())['suffix']

m1 = 'This is a test for a fake signature.' + suffix
m2 = 'My name is Zupp and I own CryptoHack.org' + suffix
m3 = 'Please send all my money to 3EovkHLK5kkAbE8Kpe53mkEbyQGjyf8ECw' + suffix

def cvt(msg):
    return bytes_to_long(emsa_pkcs1_v15.encode(msg.encode(), 768 // 8))

msg1, msg2, msg3 = cvt(m1), cvt(m2), cvt(m3)

s_mod = Mod(s, n)
e1 = discrete_log(Mod(msg1, n), s_mod)
e2 = discrete_log(Mod(msg2, n), s_mod)
e3 = discrete_log(Mod(msg3, n), s_mod)

def claim(msg, idx, e_val):
    r.sendline(dumps({'option': 'claim', 'msg': msg, 'index': idx, 'e': hex(e_val)}).encode())
    return bytes.fromhex(loads(r.recvline())['secret'])

sec1 = claim(m1, 0, e1)
sec2 = claim(m2, 1, e2)
sec3 = claim(m3, 2, e3)

flag = xor(sec1, sec2, sec3).decode()
print(f"{flag}")
