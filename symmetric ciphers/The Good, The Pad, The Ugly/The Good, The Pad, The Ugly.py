import json
from pwn import *

# Tập ký tự hex (0-9, a-f) - message chắc chắn nằm trong đây
HEX_CHARS = [ord(c) for c in "0123456789abcdef"]

def get_conn():
    r = remote('socket.cryptohack.org', 13422, level='error')
    r.recvline()
    return r

conn = get_conn()

def check_padding(payload_hex):
    global conn
    # Tăng lên 20 lần thử để loại bỏ hoàn toàn nhiễu (Noise)
    # Xác suất sai số: 0.6^20 = 0.00003 (cực thấp)
    for _ in range(20): 
        try:
            conn.sendline(json.dumps({"option": "unpad", "ct": payload_hex}).encode())
            res = json.loads(conn.recvline().decode())
            if res["result"] == False:
                return False # Thấy False là loại ngay
        except:
            conn.close()
            conn = get_conn()
            return check_padding(payload_hex)
    return True

# 1. Lấy Ciphertext mục tiêu
conn.sendline(json.dumps({"option": "encrypt"}).encode())
ct_data = json.loads(conn.recvline().decode())
ct = bytes.fromhex(ct_data["ct"])
iv, blocks = ct[:16], [ct[i:i+16] for i in range(16, len(ct), 16)]

final_res = ""
prev_block = iv

# 2. Giải mã chính xác 32 ký tự (2 khối đầu)
for b_idx in range(2):
    target = blocks[b_idx]
    print(f"\n[*] Đang giải khối {b_idx + 1}/2...")
    inter = bytearray(16)
    pt = bytearray(16)
    
    for i in range(15, -1, -1):
        pad_val = 16 - i
        fake_iv_base = bytearray(16)
        for k in range(i + 1, 16):
            fake_iv_base[k] = inter[k] ^ pad_val
            
        found = False
        for val in HEX_CHARS:
            test_byte = val ^ pad_val ^ prev_block[i]
            fake_iv = bytearray(fake_iv_base)
            fake_iv[i] = test_byte
            
            if check_padding((fake_iv + target).hex()):
                inter[i] = test_byte ^ pad_val
                pt[i] = inter[i] ^ prev_block[i]
                print(f"{chr(pt[i])}", end="", flush=True)
                found = True
                break
        
        if not found:
            # Nếu không tìm thấy trong HEX_CHARS, thử toàn bộ 256 byte (đề phòng)
            for val in range(256):
                if val in HEX_CHARS: continue
                # ... thực hiện logic tương tự ...
                
    final_res += pt.decode()
    prev_block = target

# 3. Kết quả cuối
print(f"\n\n[!] Message khôi phục (32 ký tự): {final_res}")
conn.sendline(json.dumps({"option": "check", "message": final_res}).encode())
print(f"[!] FLAG: {conn.recvline().decode()}")