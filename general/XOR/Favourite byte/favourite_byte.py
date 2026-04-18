ciphertext = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")

for key in range(256):
    plaintext = bytes(b ^ key for b in ciphertext)
    try:
        decoded = plaintext.decode('ascii')
        if decoded.startswith("crypto{"):
            print(decoded)
    except:
        pass