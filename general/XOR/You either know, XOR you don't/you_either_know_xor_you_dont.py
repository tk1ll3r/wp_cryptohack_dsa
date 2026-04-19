# Bước 0: Decode hex sang bytes
ciphertext = bytes.fromhex("0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104")
known = b"crypto{"

key_partial = bytes(c ^ p for c, p in zip(ciphertext, known))

key = b"myXORkey"
full_key = (key * ((len(ciphertext) // len(key)) + 1))[:len(ciphertext)]

plaintext = bytes(c ^ k for c, k in zip(ciphertext, full_key))
print(plaintext.decode())