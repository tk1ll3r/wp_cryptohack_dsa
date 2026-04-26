# **E. Generative AI**

## **1. Deriving Symmetric Keys**

### Prompt
![](assets/generative-ai/1.%20Deriving%20Symmetric%20Keys/1.png)
![](assets/generative-ai/1.%20Deriving%20Symmetric%20Keys/2.png)
![](assets/generative-ai/1.%20Deriving%20Symmetric%20Keys/3.png)

### Screenshot AI chat
![](assets/generative-ai/1.%20Deriving%20Symmetric%20Keys/4.png)
![](assets/generative-ai/1.%20Deriving%20Symmetric%20Keys/5.png)
![](assets/generative-ai/1.%20Deriving%20Symmetric%20Keys/6.png)
![](assets/generative-ai/1.%20Deriving%20Symmetric%20Keys/7.png)

### Code Python
```py
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

# --- Diffie-Hellman Parameters ---
p = 2410312426921032588552076022197566074856950548502459942654116941958108831682612228890093858261341614673227141477904012196503648957050582631942730706805009223062734745341073406696246014589361659774041027169249453200378729434170325843778659198143763193776859869524088940195577346119843545301547043747207749969763750084308926339295559968882457872412993810129130294592999947926365264059284647209730384947211681434464714438488520940127459844288859336526896320919633919

A = 112218739139542908880564359534373424013016249772931962692237907571990334483528877513809272625610512061159061737608547288558662879685086684299624481742865016924065000555267977830144740364467977206555914781236397216033805882207640219686011643468275165718132888489024688846101943642459655423609111976363316080620471928236879737944217503462265615774774318986375878440978819238346077908864116156831874695817477772477121232820827728424890845769152726027520772901423784

b = 197395083814907028991785772714920885908249341925650951555219049411298436217190605190824934787336279228785809783531814507661385111220639329358048196339626065676869119737979175531770768861808581110311903548567424039264485661330995221907803300824165469977099494284722831845653985392791480264712091293580274947132480402319812110462641143884577706335859190668240694680261160210609506891842793868297672619625924001403035676872189455767944077542198064499486164431451944

# --- Step 1: Compute shared secret ---
shared_secret = pow(A, b, p)  # Fast modular exponentiation

# --- Step 2: Derive AES key via SHA1 ---
sha1 = hashlib.sha1()
sha1.update(str(shared_secret).encode('ascii'))
key = sha1.digest()[:16]  # First 16 bytes = AES-128 key

# --- Step 3: Decrypt with AES-CBC ---
iv  = bytes.fromhex('737561146ff8194f45290f5766ed6aba')
ct  = bytes.fromhex('39c99bf2f0c14678d6a5416faef954b5893c316fc3c48622ba1fd6a9fe85f3dc72a29c394cf4bc8aff6a7b21cae8e12c')

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ct)

try:
    flag = unpad(plaintext, 16).decode('ascii')
except Exception:
    flag = plaintext.decode('ascii', errors='replace')

print("Flag:", flag)
```

### Flag
![](assets/generative-ai/1.%20Deriving%20Symmetric%20Keys/flag.png)

### Ảnh submit thành công
![](assets/generative-ai/1.%20Deriving%20Symmetric%20Keys/submit.png)

## **2. Parameter Injection**
### Prompt & Screenshot AI chat
- **LẦN 1**
    
    > **Prompt**
    ![](assets/generative-ai/2.%20Parameter%20Injection/1.png)

    > **AI**
    ![](assets/generative-ai/2.%20Parameter%20Injection/2.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/3.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/4.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/5.png)

- **LẦN 2**

    > **Prompt**
    ![](assets/generative-ai/2.%20Parameter%20Injection/6.png)

    > **AI**
    ![](assets/generative-ai/2.%20Parameter%20Injection/7.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/8.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/9.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/10.png)

- **LẦN 3**

    > **Prompt**
    ![](assets/generative-ai/2.%20Parameter%20Injection/11.png)

    > **AI**
    ![](assets/generative-ai/2.%20Parameter%20Injection/12.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/13.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/14.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/15.png)

- **LẦN 4**

    > **Promtp**
    ![](assets/generative-ai/2.%20Parameter%20Injection/16.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/17.png)

    > **AI**
    ![](assets/generative-ai/2.%20Parameter%20Injection/18.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/19.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/20.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/21.png)

- **LẦN 5**

    > **Prompt**
    ![](assets/generative-ai/2.%20Parameter%20Injection/22.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/23.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/24.png)

    > **AI**
    ![](assets/generative-ai/2.%20Parameter%20Injection/25.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/26.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/27.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/28.png)

- **LẦN 6**

    > **Prompt**
    ![](assets/generative-ai/2.%20Parameter%20Injection/29.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/30.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/31.png)

    > **AI**
    ![](assets/generative-ai/2.%20Parameter%20Injection/32.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/33.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/34.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/35.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/36.png)

- **LẦN 7**

    > **Prompt**
    ![](assets/generative-ai/2.%20Parameter%20Injection/37.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/38.png)

    > **AI**
    ![](assets/generative-ai/2.%20Parameter%20Injection/39.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/40.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/41.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/42.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/43.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/44.png)

- **LẦN 9**

    > **Prompt**
    ![](assets/generative-ai/2.%20Parameter%20Injection/45.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/46.png)

    > **AI**
    ![](assets/generative-ai/2.%20Parameter%20Injection/47.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/48.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/49.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/50.png)

- **LẦN 10**

    > **Prompt**
    ![](assets/generative-ai/2.%20Parameter%20Injection/51.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/52.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/53.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/54.png)

    > **AI**
    ![](assets/generative-ai/2.%20Parameter%20Injection/55.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/56.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/57.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/58.png)

- **LẦN 11**

    > **Prompt**
    ![](assets/generative-ai/2.%20Parameter%20Injection/59.png)

    > **AI**
    ![](assets/generative-ai/2.%20Parameter%20Injection/60.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/61.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/62.png)
    ![](assets/generative-ai/2.%20Parameter%20Injection/63.png)


### Code Python
```py
#!/usr/bin/env python3
import socket
import json
import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import bytes_to_long

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    try:
        return unpad(plaintext, 16).decode('ascii')
    except:
        return plaintext.decode('ascii')

def recv_until(s, token: bytes):
    """token phải là bytes, KHÔNG gọi .encode()"""
    data = b""
    while not data.endswith(token):
        data += s.recv(1)
    return data

def recvline_json(s):
    data = b""
    while True:
        byte = s.recv(1)
        data += byte
        if byte == b"\n":
            break
    line = data.decode().strip()
    print(f"[RECV] {line}")
    return json.loads(line)

def send_json(s, obj):
    msg = json.dumps(obj) + "\n"
    print(f"[SEND] {msg.strip()}")
    s.sendall(msg.encode())

def solve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('socket.cryptohack.org', 13371))
    s.settimeout(30)
    print("[*] Connected!")

    recv_until(s, b"Intercepted from Alice: ")
    alice_msg = recvline_json(s)

    p = int(alice_msg['p'], 16)
    g = int(alice_msg['g'], 16)
    A = int(alice_msg['A'], 16)
    print(f"[*] p bits={p.bit_length()}, g={g}")

    c = bytes_to_long(os.urandom(32))

    recv_until(s, b"Send to Bob: ")
    send_json(s, {"p": hex(p), "g": hex(g), "A": hex(p)})

    recv_until(s, b"Intercepted from Bob: ")
    bob_msg = recvline_json(s)

    recv_until(s, b"Send to Alice: ")
    C = pow(g, c, p)
    send_json(s, {"B": hex(C)})

    recv_until(s, b"Intercepted from Alice: ")
    enc_msg = recvline_json(s)

    shared_secret = pow(A, c, p)
    print(f"[*] shared_secret[:32] = {hex(shared_secret)[:34]}...")

    flag = decrypt_flag(shared_secret, enc_msg['iv'], enc_msg['encrypted_flag'])
    print(f"\n✅ FLAG: {flag}")
    s.close()

solve()
```

### Flag
![](assets/generative-ai/2.%20Parameter%20Injection/64.png)

### Ảnh submit thành công
![](assets/generative-ai/2.%20Parameter%20Injection/65.png)

## **3. Export-grade**
### Prompt & Screenshot AI Chat
- **LẦN 1**

    > **Prompt**
    ![](assets/generative-ai/3.%20Export-grade/1.png)

    > **AI**
    ![](assets/generative-ai/3.%20Export-grade/2.png)
    ![](assets/generative-ai/3.%20Export-grade/3.png)
    ![](assets/generative-ai/3.%20Export-grade/4.png)
    ![](assets/generative-ai/3.%20Export-grade/5.png)

- **LẦN 2**

    > **Prompt**
    ![](assets/generative-ai/3.%20Export-grade/6.png)

    > **AI**
    ![](assets/generative-ai/3.%20Export-grade/7.png)
    ![](assets/generative-ai/3.%20Export-grade/8.png)
    ![](assets/generative-ai/3.%20Export-grade/9.png)
    ![](assets/generative-ai/3.%20Export-grade/10.png)

- **LẦN 3**

    > **Prompt**
    ![](assets/generative-ai/3.%20Export-grade/11.png)

    > **AI**
    ![](assets/generative-ai/3.%20Export-grade/12.png)
    ![](assets/generative-ai/3.%20Export-grade/13.png)
    ![](assets/generative-ai/3.%20Export-grade/14.png)
    ![](assets/generative-ai/3.%20Export-grade/15.png)

### Code Python
```py
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
from pwn import *
import json
from sympy.ntheory.residue_ntheory import discrete_log

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    return plaintext.decode('ascii')

def recv_json(r):
    """Đọc từng dòng cho đến khi tìm được JSON hợp lệ."""
    while True:
        line = r.recvline(timeout=15).decode(errors='ignore').strip()
        print("[<]", line)
        if not line:
            continue
        # Tìm phần JSON trong dòng (bắt đầu từ '{')
        idx = line.find('{')
        if idx != -1:
            try:
                return json.loads(line[idx:])
            except json.JSONDecodeError:
                continue

r = remote('socket.cryptohack.org', 13379)

# ---- Bước 1: Server yêu cầu gửi cho Bob ----
# Đọc đến khi gặp "Send to Bob"
r.recvuntil(b'Send to Bob:', timeout=15)
r.sendline(b'{"supported": ["DH64"]}')
print("[>] Sent: supported DH64")

# ---- Bước 2: Đọc phần Intercepted from Bob (để lấy "chosen") ----
# rồi server yêu cầu gửi cho Alice
r.recvuntil(b'Send to Alice:', timeout=15)
r.sendline(b'{"chosen": "DH64"}')
print("[>] Sent: chosen DH64")

# ---- Bước 3: Intercepted from Alice → p, g, A ----
r.recvuntil(b'Intercepted from Alice:', timeout=15)
line = r.recvline(timeout=15).decode(errors='ignore').strip()
print("[<] Alice params:", line)
data = json.loads(line)
p = int(data["p"], 16)
g = int(data["g"], 16)
A = int(data["A"], 16)
print(f"    p = {hex(p)}\n    g = {hex(g)}\n    A = {hex(A)}")

# ---- Bước 4: Intercepted from Bob → B ----
r.recvuntil(b'Intercepted from Bob:', timeout=15)
line = r.recvline(timeout=15).decode(errors='ignore').strip()
print("[<] Bob pubkey:", line)
data = json.loads(line)
B = int(data["B"], 16)
print(f"    B = {hex(B)}")

# ---- Bước 5: Intercepted from Alice → encrypted flag ----
r.recvuntil(b'Intercepted from Alice:', timeout=15)
line = r.recvline(timeout=15).decode(errors='ignore').strip()
print("[<] Encrypted flag:", line)
data = json.loads(line)
iv = data["iv"]
ciphertext = data["encrypted_flag"]

# ---- Giải discrete log (p là 64-bit, rất nhanh) ----
print("[*] Solving discrete log...")
a = discrete_log(p, A, g)
print(f"[*] a = {a}")

shared_secret = pow(B, a, p)
print(f"[*] Shared secret = {shared_secret}")
print("[+] Flag:", decrypt_flag(shared_secret, iv, ciphertext))
```

### Flag
![](assets/generative-ai/3.%20Export-grade/16.png)

### Ảnh submit thành công
![](assets/generative-ai/3.%20Export-grade/17.png)


## **ĐÁNH GIÁ TIỀM NĂNG VÀ HẠN CHẾ CỦA GENERATIVE AI TRONG CRYPTANALYSIS**

- Dựa trên trải nghiệm thực tế khi giải ba challenge Diffie–Hellman, tôi cho rằng Generative AI có tiềm năng rất lớn trong cryptanalysis, nhưng chủ yếu ở vai trò công cụ hỗ trợ hơn là thay thế hoàn toàn nhà phân tích. Điểm mạnh rõ nhất của AI là khả năng tăng tốc quá trình hiểu đề, nhắc lại kiến thức nền, đề xuất hướng tấn công và sinh nhanh mã thử nghiệm. Trong các challenge đã làm, AI giúp rút ngắn đáng kể thời gian từ lúc đọc đề đến lúc hình thành ý tưởng như parameter injection, man-in-the-middle hay hạ cấp tham số xuống mức yếu. Điều này phù hợp với nhận định chung rằng Generative AI có thể tự động hóa nhiều tác vụ kỹ thuật, hỗ trợ lập trình và tăng tốc xử lý công việc phức tạp.

- Tuy nhiên, trải nghiệm thực tế cũng cho thấy AI chưa đủ đáng tin để tự giải bài toán mật mã một cách chính xác từ đầu đến cuối. Trong quá trình làm challenge, AI nhiều lần suy đoán sai về format giao thức, thứ tự message, cách server xử lý negotiation, hoặc phương pháp derive shared secret. Các câu trả lời thường nghe rất hợp lý, nhưng khi chạy code thì phát sinh lỗi hoặc đi sai hướng. Đây là hạn chế quen thuộc của Generative AI: đầu ra có thể trôi chảy và thuyết phục nhưng vẫn sai bản chất, nên luôn cần con người kiểm tra lại bằng log, kiến thức toán học và thử nghiệm thực tế.

- Một điểm hạn chế khác là AI mạnh ở mức ý tưởng tổng quát nhưng yếu ở các chi tiết quyết định thành bại. Trong cryptanalysis, chỉ một sai khác nhỏ về JSON format, hướng truyền message hay giả định bên nào thực hiện mã hóa cũng đủ làm toàn bộ lời giải thất bại. AI có thể hỗ trợ sinh mã và gợi ý nhiều hướng thử, nhưng việc xác minh từng giả thuyết, đọc dấu hiệu từ output và sửa lỗi theo ngữ cảnh thực vẫn phụ thuộc rất lớn vào người dùng. Nói cách khác, AI giúp mở rộng không gian tìm kiếm lời giải, nhưng chưa thể thay thế tư duy phản biện và khả năng kiểm chứng của con người.

- Vì vậy, đánh giá công bằng nhất là Generative AI rất hữu ích trong cryptanalysis khi được dùng như một “trợ lý kỹ thuật”: hỗ trợ giải thích thuật toán, sinh mã mẫu, gợi ý chiến lược tấn công và tăng tốc vòng lặp thử–sai. Tuy nhiên, nó không nên được xem là nguồn chân lý cuối cùng, đặc biệt trong những bài toán đòi hỏi độ chính xác cao như phân tích giao thức mật mã. Hiệu quả tốt nhất chỉ đạt được khi kết hợp AI với kiến thức nền tảng, khả năng debug và kiểm chứng chặt chẽ của con người.