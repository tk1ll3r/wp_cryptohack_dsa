from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.number import *
from Crypto.Util.Padding import pad, unpad

import json

p = 13322168333598193507807385110954579994440518298037390249219367653433362879385570348589112466639563190026187881314341273227495066439490025867330585397455471
N = 30

def load_matrix(fname):
    data = open(fname, 'r').read().strip()
    rows = [list(map(int, row.split(' '))) for row in data.splitlines()]
    return Matrix(GF(p), rows)

G = load_matrix("/home/sage/chal/generator.txt")
output = json.loads(open("/home/sage/chal/output.txt").read())

v = Matrix(GF(p), output['v'])
w = Matrix(GF(p), output['w']) # w = G^k v

J, P = G.jordan_form(transformation=True) # G = P J P^-1

# => w = P J^k P^-1 v
# => P^-1 w = J^k (P^-1 v)
# let w_ = LHS, v_ = P^-1 v

w_ = (P^(-1)) * (w.T)
v_ = (P^(-1)) * (v.T)

# Note that the lower 2x2 block of J is of the form [[n,1],[0,n]] and that
# [[n,1],[0,n]]^k = n^(k-1) [[n,k],[0,n]]

# let w_ = [...,w1, w2], v_ = [...,v1,v2]
# letting [w1, w2] = [[n,1],[0,n]]^k [v1, v2] and solving the resulting system of equations
# we get that k = n/w2 (w1 - w2*v1/v2)
M = J[-2:,-2:]
n = M[0,0]
v1, v2 = list(v_.T)[0][-2:]
w1, w2 = list(w_.T)[0][-2:]

SECRET = int(n/w2 * (w1 - w2*v1/v2))

# Decrypt the flag

KEY_LENGTH = 128
KEY = SHA256.new(data=str(SECRET).encode()).digest()[:KEY_LENGTH]

flag_enc = json.loads(open("/home/sage/chal/flag.enc", "r").read())
cipher = AES.new(KEY, AES.MODE_CBC, iv=bytes.fromhex(flag_enc["iv"]))

print(cipher.decrypt(bytes.fromhex(flag_enc["ciphertext"])))
