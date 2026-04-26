from pwn import *
import json
import sys

# Kết nối
r = remote('socket.cryptohack.org', 13423)
r.recvuntil(b'harder!\n')

def get_encryption():
    r.sendline(json.dumps({"option": "encrypt"}).encode())
    return bytes.fromhex(json.loads(r.readline())['ct'])

def get_best_candidate(target_ct, prefix, suffix, pad_val, prev_block, i):
    # Chỉ tập trung vào 16 ký tự hợp lệ của bảng mã Hex
    active = list(b'0123456789abcdef')
    scores = {c: 0 for c in active}
    queries_used = 0
    
    while True:
        # Gửi tuần tự từng ứng viên còn trụ lại trong danh sách
        for c in active:
            b = prev_block[16-i] ^ c ^ pad_val
            test_iv = prefix + bytes([b]) + suffix
            ct_hex = (test_iv + target_ct).hex()
            
            r.sendline(json.dumps({"option": "unpad", "ct": ct_hex}).encode())
            
            try:
                res = json.loads(r.readline())['result']
            except Exception as e:
                print(f"\n[-] Server ngắt kết nối đột ngột tại lượt {queries_used}. Vui lòng chạy lại!")
                sys.exit(1)
                
            # Oracle: True -> padding sai (40% trả về False), False -> padding đúng (60% trả về False)
            # Do đó nếu nhận False, ta cộng điểm.
            if res == False:
                scores[c] += 1
            else:
                scores[c] -= 1
                
            queries_used += 1

        # Cập nhật điểm cao nhất hiện tại
        max_score = max([scores[c] for c in active])
        
        # LỌC THÍCH NGHI: Loại ngay các ứng viên thua leader quá 6 điểm
        active = [c for c in active if scores[c] >= max_score - 6]
        
        # ĐIỀU KIỆN CHỐT 1: Chỉ còn đúng 1 ứng viên sống sót và đã test đủ độ tin cậy
        if len(active) == 1 and queries_used >= 15:
            return active[0]
            
        # ĐIỀU KIỆN CHỐT 2: Leader bỏ xa người thứ hai 7 điểm -> Chắc chắn đúng
        if len(active) >= 2:
            sorted_scores = sorted([scores[c] for c in active], reverse=True)
            if sorted_scores[0] - sorted_scores[1] >= 7:
                return max(active, key=lambda x: scores[x])
                
        # CHỐT CHẶN AN TOÀN: Đảm bảo không bao giờ kẹt vòng lặp vô tận (giới hạn 300 lượt/byte)
        if queries_used > 300:
            return max(active, key=lambda x: scores[x])

def decrypt_block(target_ct, prev_block):
    decrypted = bytearray(16)
    
    for i in range(1, 17):
        pad_val = i
        prefix = prev_block[:16-i]
        
        suffix = bytearray()
        for j in range(1, i):
            suffix.append(prev_block[16-j] ^ decrypted[16-j] ^ pad_val)
        suffix = suffix[::-1]
        
        best_c = get_best_candidate(target_ct, prefix, suffix, pad_val, prev_block, i)
        
        decrypted[16-i] = best_c
        print(f"[*] Found byte {16-i:02d}: '{chr(best_c)}' | Giải mã dần: {decrypted[16-i:].decode('ascii', errors='ignore')}")
        
    return decrypted

print("[+] Đang lấy Ciphertext mục tiêu...")
target_ct_full = get_encryption()

# Cắt Ciphertext ra thành các Block (mỗi block 16 bytes)
blocks = [target_ct_full[i:i+16] for i in range(0, len(target_ct_full), 16)]

print("\n[+] Đang giải mã Block 2 (16 ký tự cuối)...")
msg2 = decrypt_block(blocks[2], blocks[1])

print("\n[+] Đang giải mã Block 1 (16 ký tự đầu)...")
msg1 = decrypt_block(blocks[1], blocks[0])

# Ráp thành chuỗi rõ ban đầu
final_msg = (msg1 + msg2).decode('ascii')
print(f"\n[+] BẢN RÕ ĐÃ KHÔI PHỤC: {final_msg}")

print("[+] Gửi kết quả lên server để lấy Flag...")
r.sendline(json.dumps({"option": "check", "message": final_msg}).encode())

try:
    response = r.recvall(timeout=3).decode()
    print("\n[+] FLAG:\n" + response)
except Exception as e:
    print(f"[-] Có lỗi khi nhận cờ: {e}")