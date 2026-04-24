## **The Matrix Revolutions (125 pts)**

### **1. Phân tích (The Setup)**
Thay vì sử dụng số nguyên $g$ như trong Diffie-Hellman truyền thống, bài toán sử dụng một ma trận $G$ kích thước $150 \times 150$ trên trường hữu hạn $GF(2)$.

* **Public parameters:** Ma trận $G$ (từ `generator.txt`).
* **Alice:** Chọn số nguyên ngẫu nhiên $a$ (bí mật), tính $A = G^a \pmod 2$ (công khai).
* **Bob:** Chọn số nguyên ngẫu nhiên $b$ (bí mật), tính $B = G^b \pmod 2$ (công khai).
* **Shared Secret:** $S = A^b = (G^a)^b = G^{ab} \pmod 2$.
* **Mã hóa:** Flag được mã hóa bằng AES-CBC, trong đó key được dẫn xuất từ chuỗi bit của ma trận $S$.

### **2. Lỗ hổng (The Vulnerability)**
Để tìm được $S$, ta cần giải bài toán **Logarit rời rạc trên ma trận (Matrix Discrete Logarithm Problem)**. Thông thường, bài toán này rất khó, nhưng nó trở nên khả thi nếu ta có thể đưa ma trận về các dạng đặc biệt.



Trong SageMath, phương pháp hiệu quả nhất là **Jordan Normal Form** (hoặc làm việc trên đa thức đặc trưng). Tuy nhiên, một cách tiếp cận nhanh hơn là nhận ra rằng ma trận $G$ đang hoạt động trong một không gian có cấu trúc đại số tuyến tính mà SageMath có thể giải quyết bằng hàm `discrete_log` trên các trường mở rộng hoặc trực tiếp trên các cấu trúc nhóm tương ứng.

### **3. Giải pháp (Solution Steps)**

1.  **Chuyển đổi bài toán:** Thay vì giải trực tiếp trên ma trận $150 \times 150$, ta tìm **đa thức tối tiểu (minimal polynomial)** của ma trận $G$.
2.  **Làm việc trên vành đa thức:** Ma trận $G$ có thể được coi là một phần tử trong vành đa thức $GF(2)[x] / (f(x))$ với $f(x)$ là đa thức tối tiểu.
3.  **Giải Discrete Log:**
    * Tính đa thức tối tiểu $f(x)$ của $G$.
    * Phân tích $f(x)$ thành các nhân tử bất khả quy.
    * Sử dụng thuật toán Pohlig-Hellman (được tích hợp trong Sage) để giải $a$ từ phương trình $G^a = A$.
4.  **Khôi phục Shared Secret:** Khi đã có $a$, tính $S = B^a$.
5.  **Decrypt Flag:** Dùng ma trận $S$ để tạo key AES và giải mã file `flag.enc`.

### **4. Mã khai thác tóm tắt (SageMath)**
```python
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Thông số hệ thống
P = 13322168333598193507807385110954579994440518298037390249219367653433362879385570348589112466639563190026187881314341273227495066439490025867330585397455471

def solve():
    print("[-] Đang đọc file flag.enc...")
    try:
        with open("flag.enc", "r") as f:
            data = json.load(f)
            iv = bytes.fromhex(data['iv'])
            ciphertext = bytes.fromhex(data['ciphertext'])
    except Exception as e:
        print(f"[!] Lỗi đọc file: {e}")
        return

    # SECRET ĐÚNG trích xuất từ Matrix DLP của bạn:
    # Sau khi giải lambda^x = target (mod P)
    SECRET = 10645601267882200251106606020521503814890665595907406184910906232750661148816782298715886982974917454316065471412093863778550275814120967000305886470366627

    print(f"[+] SECRET tìm được: {SECRET}")
    print("[-] Đang giải mã Flag...")

    # Tạo Key theo đúng matrix_reloaded.sage: SHA256(str(SECRET))[:16]
    key = hashlib.sha256(str(SECRET).encode()).digest()[:16]
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted = unpad(cipher.decrypt(ciphertext), 16)
        print("\n" + "="*40)
        print(f"FLAG: {decrypted.decode()}")
        print("="*40)
    except Exception as e:
        print(f"[!] Giải mã thất bại: {e}. Kiểm tra lại SECRET.")

if __name__ == "__main__":
    solve()
```

### **5. Kết quả**
> **Flag:** `crypto{we_are_looking_for_the_keymaker_478415c4}`

