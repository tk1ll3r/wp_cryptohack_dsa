import requests
from pwn import xor

BASE = "https://aes.cryptohack.org"

def encrypt(pt_hex):
    # Mã hóa plaintext hex bằng AES-CBC (IV = KEY trên server).
    r = requests.get(f"{BASE}/lazy_cbc/encrypt/{pt_hex}/")
    return r.json()["ciphertext"]

def receive(ct_hex):
    # Gửi ciphertext lên server, trả về error message nếu plaintext không phải ASCII.
    r = requests.get(f"{BASE}/lazy_cbc/receive/{ct_hex}/")
    return r.json()

def get_flag(key_hex):
    # Lấy flag nếu cung cấp đúng key.
    r = requests.get(f"{BASE}/lazy_cbc/get_flag/{key_hex}/")
    return bytes.fromhex(r.json()["plaintext"]).decode()


# Bước 1: Mã hóa 2 block plaintext bất kỳ -> lấy C0, C1
plaintext = b"a" * 32
ct = encrypt(plaintext.hex())
C0 = ct[:32]   # block 0 của ciphertext

# Bước 2: Gửi ciphertext bẫy [C0 | C0] lên receive
fake_ct = C0 + C0
result = receive(fake_ct)

# Server trả lỗi vì P'_1 không phải ASCII -> lộ toàn bộ plaintext dạng hex
leaked_plaintext = bytes.fromhex(result["error"].split(": ")[1])
P0_leaked = leaked_plaintext[:16]   # P'_0 = "a" * 16
P1_leaked = leaked_plaintext[16:]   # P'_1 = AES_Decrypt(C0) ⊕ C0

# Bước 3: Tính KEY = P'_1 ⊕ P_0 ⊕ C0
P0       = b"a" * 16
C0_bytes = bytes.fromhex(C0)
KEY      = xor(P1_leaked, P0, C0_bytes)
print(f"KEY: {KEY.hex()}")

# Bước 4: Dùng KEY để lấy flag
print(get_flag(KEY.hex()))