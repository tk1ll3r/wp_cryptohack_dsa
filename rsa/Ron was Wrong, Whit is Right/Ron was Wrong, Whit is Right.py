import os
from math import gcd
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Lấy đường dẫn thư mục hiện tại (nơi bạn đang đứng trong Terminal)
current_dir = os.getcwd() 

def solve():
    keys = []
    ciphertexts = {}

    print(f"[*] Đang tìm file tại: {current_dir}")

    # 1. Đọc dữ liệu
    for i in range(1, 51):
        pem_path = os.path.join(current_dir, f"{i}.pem")
        cit_path = os.path.join(current_dir, f"{i}.ciphertext")
        
        if os.path.exists(pem_path) and os.path.exists(cit_path):
            with open(pem_path, 'r') as f:
                key = RSA.import_key(f.read())
            with open(cit_path, 'r') as f:
                c_hex = f.read().strip()
            
            # Sửa lỗi in ấn ở đây: ép kiểu sang string trước khi cắt [:20]
            print(f"[+] Đã đọc: {i}.pem - Modulus: {str(key.n)[:20]}...")
            
            keys.append({'id': i, 'n': key.n, 'e': key.e})
            ciphertexts[i] = bytes.fromhex(c_hex)

    if not keys:
        print("[-] Vẫn không thấy file nào. Bạn có chắc file nằm trong thư mục 'Pemfile' không?")
        return

    # 2. Tấn công Batch GCD
    print(f"[*] Đang so sánh {len(keys)} khóa để tìm GCD...")
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            n1, n2 = keys[i]['n'], keys[j]['n']
            p = gcd(n1, n2)
            
            if 1 < p < n1:
                print(f"\n[!] BINGO! Tìm thấy ước chung p giữa file {keys[i]['id']} và {keys[j]['id']}")
                
                # Giải mã
                for target in [keys[i], keys[j]]:
                    n, e, idx = target['n'], target['e'], target['id']
                    q = n // p
                    phi = (p - 1) * (q - 1)
                    d = pow(e, -1, phi)
                    
                    priv_key = RSA.construct((n, e, d, p, q))
                    cipher = PKCS1_OAEP.new(priv_key)
                    
                    try:
                        flag = cipher.decrypt(ciphertexts[idx])
                        print(f"===> FLAG ({idx}): {flag.decode()}")
                    except:
                        continue
                return

if __name__ == "__main__":
    solve()