import requests
from pwn import xor

BASE = "https://aes.cryptohack.org"

def get_cookie():
    # Lấy IV + ciphertext CBC từ server.
    r = requests.get(f"{BASE}/flipping_cookie/get_cookie/")
    return r.json()["cookie"]

def check_admin(cookie_hex, iv_hex):
    # Gửi cookie đã chỉnh lên server để kiểm tra admin.
    r = requests.get(f"{BASE}/flipping_cookie/check_admin/{cookie_hex}/{iv_hex}/")
    return r.json()

# Bước 1: Lấy cookie và tách IV, ciphertext
cookie_hex = get_cookie()
iv  = bytes.fromhex(cookie_hex[:32])  # 16 bytes đầu là IV
ct  = cookie_hex[32:]                 # phần ciphertext (giữ nguyên)

# Bước 2: Tính IV mới để flip "admin=False" -> "admin=True"
# Plaintext block 0 gốc (16 byte đầu của "admin=False;expiry=...")
P0_original = b"admin=False;expi"
# Plaintext block 0 mong muốn sau khi decrypt
P0_target   = b"admin=True;\x00\x00\x00\x00\x00"

# IV' = IV ⊕ P0_original ⊕ P0_target
iv_new = xor(iv, P0_original, P0_target)

# Bước 3: Gửi ciphertext gốc với IV mới
result = check_admin(ct, iv_new.hex())
print(result)