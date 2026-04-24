import requests
from concurrent.futures import ThreadPoolExecutor
import string

BASE_URL = "https://aes.cryptohack.org/oh_snap"
session = requests.Session()

def get_keystream_byte(nonce_hex):
    url = f"{BASE_URL}/send_cmd/00/{nonce_hex}/"
    try:
        r = session.get(url, timeout=5)
        res = r.json()
        if "error" in res:
            return int(res["error"].split(": ")[1], 16)
    except:
        return None
    return None

def solve():
    known_key = []
    print("--- Bắt đầu khôi phục FLAG (Chế độ chính xác cao) ---")

    for a in range(45): # Quét độ dài tối đa 45
        prob = [0] * 256
        # Dùng đủ 256 mẫu để đảm bảo không bị sai byte cuối
        samples = range(256) 
        nonces = [bytes([a + 3, 255, x]).hex() for x in samples]
        
        # Gửi 10 luồng cùng lúc để không quá nhanh gây lỗi server
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(get_keystream_byte, nonces))
        
        for x, z in enumerate(results):
            if z is None: continue
            
            iv = [a + 3, 255, x]
            # Giả lập KSA
            S = list(range(256))
            j = 0
            for i in range(3):
                j = (j + S[i] + iv[i]) % 256
                S[i], S[j] = S[j], S[i]
            
            # Trộn với các byte đã tìm được chính xác
            for i in range(a):
                j = (j + S[i+3] + known_key[i]) % 256
                S[i+3], S[j] = S[j], S[i+3]
            
            # Dự đoán byte khóa
            # FLAG[a] = (z - j - S[a+3]) % 256
            key_byte = (z - j - S[a+3]) % 256
            prob[key_byte] += 1
        
        # Lấy top các ứng cử viên
        candidates = sorted(range(256), key=lambda k: prob[k], reverse=True)
        
        # Lọc: Flag của Cryptohack chỉ chứa ký tự in được
        best_byte = candidates[0]
        for cand in candidates[:10]:
            if chr(cand) in (string.ascii_letters + string.digits + "{}_!?"):
                best_byte = cand
                break
        
        known_key.append(best_byte)
        res_flag = "".join(map(chr, known_key))
        print(f"Byte {a:02d}: {chr(best_byte)} | Hiện tại: {res_flag}")
        
        if chr(best_byte) == '}':
            break

    print("\n>>> FLAG CUỐI CÙNG: " + "".join(map(chr, known_key)))

if __name__ == "__main__":
    solve()