from hashlib import sha1
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Shared Secret đã tính được từ SageMath
shared_secret = 83201481069630956436480435779471169630605662777874697301601848920266492

# Dữ liệu từ output.txt
iv_hex = '64bc75c8b38017e1397c46f85d4e332b'
enc_flag_hex = '13e4d200708b786d8f7c3bd2dc5de0201f0d7879192e6603d7c5d6b963e1df2943e3ff75f7fda9c30a92171bbbc5acbf'

# 1. Tạo khóa AES từ shared secret (theo source.py)
key = sha1(str(shared_secret).encode('ascii')).digest()[:16]

# 2. Chuyển dữ liệu hex sang bytes
iv = bytes.fromhex(iv_hex)
ciphertext = bytes.fromhex(enc_flag_hex)

# 3. Giải mã
cipher = AES.new(key, AES.MODE_CBC, iv)
try:
    decrypted = cipher.decrypt(ciphertext)
    # Gỡ padding PKCS#7
    flag = unpad(decrypted, 16)
    print("----------------------------------------")
    print(f"FLAG: {flag.decode()}")
    print("----------------------------------------")
except Exception as e:
    print(f"Lỗi khi giải mã: {e}")