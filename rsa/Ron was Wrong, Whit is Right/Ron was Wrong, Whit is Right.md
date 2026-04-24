

## **Ron was Wrong, Whit is Right (90 pts)**

### **1. Phân tích (Given)**
* **Dữ liệu:** Một file zip chứa 50 cặp file (khóa công khai `.pem` và bản mã `.ciphertext`).
* **Giao thức:** Sử dụng RSA với chuẩn mã hóa PKCS#1 OAEP.
* **Tên bài toán:** "Ron" (Rivest) và "Whit" (Diffie) ám chỉ các nhà sáng lập RSA và Diffie-Hellman. Lỗi này thường liên quan đến cách sinh số ngẫu nhiên kém dẫn đến trùng lặp.

### **2. Mục tiêu (Goal)**
* Phân tích 50 Modulus $N_i$ để tìm xem có cặp nào dùng chung số nguyên tố hay không. Nếu có, ta có thể phân tích thừa số $N$ ngay lập tức.

### **3. Giải pháp (Solution)**

#### **Lỗ hổng Batch GCD**
Nếu hai Modulus $N_1 = p \cdot q_1$ và $N_2 = p \cdot q_2$ dùng chung một số nguyên tố $p$, ta có thể tìm ra $p$ cực nhanh bằng cách tính:
$$p = \text{gcd}(N_1, N_2)$$
Sau khi có $p$, ta tìm được $q_1 = N_1 / p$ và $q_2 = N_2 / p$. Từ đó tính được số mũ giải mã $d$ cho cả hai khóa.



#### **Các bước thực hiện (Dựa trên code giải của bạn)**
1. **Thu thập:** Đọc tất cả 50 file `.pem` để lấy danh sách các số $N_i$ và $e_i$.
2. **So sánh cặp:** Duyệt qua tất cả các cặp $(N_i, N_j)$. Với mỗi cặp, tính `gcd(Ni, Nj)`.
3. **Kiểm tra:** Nếu kết quả $gcd > 1$, ta đã tìm thấy số nguyên tố dùng chung $p$.
4. **Giải mã:**
   * Tính $q = N_i / p$.
   * Tính $\phi(N_i) = (p-1)(q-1)$.
   * Tính $d = e_i^{-1} \pmod{\phi(N_i)}$.
   * Sử dụng thư viện `Crypto.Cipher.PKCS1_OAEP` để giải mã file `.ciphertext` tương ứng.

### **4. Kết quả**
Khi chạy script, bạn sẽ tìm thấy một vài cặp khóa bị lỗi "vòng lặp sinh số ngẫu nhiên" và dùng chung $p$. Giải mã các file này sẽ thu được Flag.

``` python
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
```
`crypto{3ucl1d_w0uld_b3_pr0ud}`