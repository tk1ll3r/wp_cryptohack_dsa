from pwn import *
import json
import time

# Danh sách ký tự hex để ưu tiên tìm kiếm (tăng tốc 10 lần)
HEX_CHARS = [ord(c) for c in "0123456789abcdef"]
SEARCH_SPACE = HEX_CHARS + [i for i in range(256) if i not in HEX_CHARS]

def get_connection():
    while True:
        try:
            r = remote('socket.cryptohack.org', 13421, level='error')
            r.recvline() # Bỏ banner chào mừng
            return r
        except:
            print("[!] Lỗi kết nối, thử lại sau 3s...")
            time.sleep(3)

conn = get_connection()

def oracle(ct_hex):
    global conn
    while True:
        try:
            conn.sendline(json.dumps({"option": "unpad", "ct": ct_hex}).encode())
            line = conn.recvline()
            if not line: raise EOFError
            return json.loads(line.decode())["result"]
        except:
            conn.close()
            conn = get_connection()

# 1. Lấy Ciphertext mục tiêu
conn.sendline(json.dumps({"option": "encrypt"}).encode())
ct_hex = json.loads(conn.recvline().decode())["ct"]
ct_bytes = bytes.fromhex(ct_hex)
iv = ct_bytes[:16]
# self.message.hex() có 32 ký tự -> 32 bytes ASCII -> Cần 2 blocks dữ liệu + 1 block padding
blocks = [ct_bytes[i:i+16] for i in range(16, len(ct_bytes), 16)]

# 2. Giải mã Padding Oracle
final_decrypted_bytes = []
prev_block = iv

print(f"[*] Ciphertext: {ct_hex}")

for b_idx, target_block in enumerate(blocks):
    print(f"\n[*] Giải khối {b_idx + 1}/{len(blocks)}...")
    intermediate = bytearray(16)
    block_pt = bytearray(16)
    
    for i in range(15, -1, -1):
        pad_val = 16 - i
        fake_iv = bytearray(16)
        
        # Thiết lập các byte đã giải mã để tạo padding mong muốn
        for k in range(i + 1, 16):
            fake_iv[k] = intermediate[k] ^ pad_val
            
        for val in SEARCH_SPACE:
            # Tính toán byte IV giả để sau giải mã byte tại i bằng pad_val
            # Giúp tìm ra trạng thái trung gian
            test_byte = val ^ pad_val ^ prev_block[i]
            fake_iv[i] = test_byte
            
            if oracle((fake_iv + target_block).hex()):
                # Kiểm tra tránh trường hợp pad=1 vô tình trùng pad=2,3...
                if pad_val == 1:
                    fake_iv[i-1] ^= 1
                    if not oracle((fake_iv + target_block).hex()):
                        continue
                
                intermediate[i] = test_byte ^ pad_val
                block_pt[i] = intermediate[i] ^ prev_block[i]
                print(f"    [+] Byte {i:02d}: {chr(block_pt[i])}")
                break
                
    final_decrypted_bytes.extend(block_pt)
    prev_block = target_block

# 3. Xử lý kết quả cuối cùng
full_plaintext = bytes(final_decrypted_bytes)
# Gỡ padding PKCS#7
pad_len = full_plaintext[-1]
if pad_len < 16:
    message = full_plaintext[:-pad_len].decode()
else:
    message = full_plaintext.decode() # Trường hợp hiếm không có pad block

print(f"\n[!] Message khôi phục: {message}")

# Gửi message để lấy Flag
conn.sendline(json.dumps({"option": "check", "message": message}).encode())
print(f"[*] Kết quả từ server: {conn.recvline().decode()}")