import os
import hashlib
import requests
from Crypto.Cipher import AES

# Bước 1: Tải file từ điển (giống file trên server)
current_dir = os.path.dirname(os.path.abspath(__file__))
words_path = os.path.join(current_dir, "words.txt")

if not os.path.exists(words_path):
    url = "https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words"
    response = requests.get(url)
    with open(words_path, "w") as f:
        f.write(response.text)

# Bước 2: Lấy ciphertext từ server
r = requests.get("https://aes.cryptohack.org/passwords_as_keys/encrypt_flag/")
ciphertext_hex = r.json()["ciphertext"]
print(f"Ciphertext: {ciphertext_hex}")

# Bước 3: Đọc toàn bộ từ điển
with open(words_path) as f:
    words = [w.strip() for w in f.readlines()]

# Bước 4: Brute-force — thử MD5 hash của từng từ làm key
for word in words:
    # Tạo key bằng MD5 hash của từ, giống logic server
    key = hashlib.md5(word.encode()).digest()

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(bytes.fromhex(ciphertext_hex))

    # Kiểm tra known plaintext: flag luôn bắt đầu bằng "crypto{"
    if plaintext.startswith(b"crypto{"):
        print(f"Password: {word}")
        print(f"Flag: {plaintext.decode()}")
        break
else:
    print("Không tìm thấy flag trong từ điển.")