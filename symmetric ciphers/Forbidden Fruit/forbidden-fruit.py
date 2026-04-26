import requests

BASE = "https://aes.cryptohack.org/forbidden_fruit"
P = (1 << 128) | (1 << 7) | (1 << 2) | (1 << 1) | 1
MASK = (1 << 128) - 1
def reverse_bits_128(x):
    return int(f"{x:0128b}"[::-1], 2)

def block_to_poly(hex_block):
    return reverse_bits_128(int(hex_block, 16))

def poly_to_block(x):
    return f"{reverse_bits_128(x):032x}"

def gf_mul(a, b):
    res = 0
    while b:
        if b & 1:
            res ^= a
        b >>= 1
        a <<= 1
        if a >> 128:
            a ^= P
    return res & MASK

def gf_pow(a, n):
    res = 1
    while n:
        if n & 1:
            res = gf_mul(res, a)
        a = gf_mul(a, a)
        n >>= 1
    return res

def gf_inv(a):
    if a == 0:
        raise ZeroDivisionError("zero has no inverse in GF(2^128)")
    return gf_pow(a, (1 << 128) - 2)

def api(path):
    r = requests.get(BASE + path, timeout=10)
    r.raise_for_status()
    return r.json()

def encrypt(plaintext):
    return api(f"/encrypt/{plaintext.hex()}/")

def decrypt(nonce, ciphertext, tag, associated_data):
    return api(f"/decrypt/{nonce}/{ciphertext}/{tag}/{associated_data}/")

def main():
    m1 = b"\x00" * 16
    m2 = b"\x01" * 16

    r1 = encrypt(m1)
    r2 = encrypt(m2)

    c1 = block_to_poly(r1["ciphertext"])
    c2 = block_to_poly(r2["ciphertext"])
    t1 = block_to_poly(r1["tag"])
    t2 = block_to_poly(r2["tag"])

    # For equal nonce, AAD, and 1-block messages:
    # tag1 + tag2 = (c1 + c2) * H^2 in GF(2^128).
    h2 = gf_mul(t1 ^ t2, gf_inv(c1 ^ c2))
    mask = t1 ^ gf_mul(c1, h2)

    target = encrypt(b"give me the flag")
    forged_tag = poly_to_block(gf_mul(block_to_poly(target["ciphertext"]), h2) ^ mask)

    out = decrypt(
        r1["nonce"],
        target["ciphertext"],
        forged_tag,
        r1["associated_data"],
    )
    print(bytes.fromhex(out["plaintext"]).decode())

if __name__ == "__main__":
    main()
