import requests
from PIL import Image
from json import loads
from pwn import xor
import io

def encrypt():
    print("[*] Đang tải bản mã từ server...")
    url = 'https://aes.cryptohack.org/bean_counter/encrypt'
    r = requests.get(url)
    enc = loads(r.text)['encrypted']
    return bytes.fromhex(enc)

# 1. Định nghĩa 16 bytes chuẩn của Header file PNG
png_magic_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'

# 2. Lấy toàn bộ Ciphertext
ct = encrypt()

# 3. Tìm Keystream 16-byte lặp lại bằng cách XOR 16 byte đầu của CT với Magic Bytes
print("[*] Đang tính toán Keystream...")
keystream = xor(png_magic_bytes, ct[:16])
assert len(keystream) == 16

# 4. Giải mã toàn bộ ảnh (hàm xor của pwntools tự động lặp lại keystream cho vừa độ dài ct)
print("[*] Đang giải mã và xuất file ảnh...")
png_flag = xor(keystream, ct)

# Lưu thành file flag.png
with open('flag.png', 'wb') as f:
    f.write(png_flag)

print("[🎉] Đã lưu thành công flag.png! Đang mở ảnh...")
# Mở ảnh trực tiếp để xem Flag
image = Image.open('flag.png')
image.show()