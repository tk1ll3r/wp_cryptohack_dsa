### Diffie Hellman
---
> #### 7. Export-grade

> Solution

- Vì bạn kiểm soát hoàn toàn đường truyền (Man-in-the-Middle), bạn có thể mặc kệ Bob. 
- Hãy chặn phản hồi của Bob và gửi cho Alice một Public Key giả mạo: {"B": "0x01"}.Theo thuật toán Diffie-Hellman, Alice sẽ tính khóa phiên (Shared Secret) dựa trên khóa $B$ nhận được:$$K = B^a \pmod p$$
- Do ta đã ép $B = 1$, phép tính trở thành $1^a \pmod p = 1$.$\rightarrow$ Shared Secret chắc chắn bằng 1.
- Giờ bạn đã biết chính xác Shared Secret là 1, chỉ cần dùng nó cùng với iv và encrypted_flag thu được trên đường truyền, ném vào script decrypt.py (của bài Diffie-Hellman Starter 5) là Flag sẽ hiện ra!

```
~$ nc socket.cryptohack.org 13371

Intercepted from Alice: {"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", "g": "0x02", "A": "0x56cfad49f8b300c3cd07f7316443438f207ef462139ec10db021379fc6be5b39fc4e8b1953a17399740f90214eaef6d504e2ccad0cdd6d971f6a8ec2f37d58f47a6b2bcba4921fa9e646cf19da91980d4cc7bd9627cb6ff94ec956aebd58d194233702aff44285e6bdf19614dcea89ed11a6bfa379d7d22f4bd77d4db3bcb40f00d5778ee4bf88bb71a31240b371a8b617c6607489b3024ddfdec5b7fdf4e8d0c8e07a740f07a4fd78cba008c0583c4dffd374b5f4950002b73711c02b1b7d4b"}

Send to Bob: {"p": "0x01", "g": "0x01", "A": "0x01"} 

Intercepted from Bob: {"B": "0x0"}

Send to Alice: {"B": "0x01"}

Intercepted from Alice: {"iv": "7fe6ab5b6572ad7eba0d1970a610916e", "encrypted_flag": "2c45af1150e551260525e33e7d4c38c27769ccb5ce99297ae8718fac5e571f55"}
```


---
> #### 8. Static Client

> Given

- Giao thức Diffie-Hellman không xác thực tham số đầu vào. Kẻ tấn công MitM có quyền chặn, chỉnh sửa các tham số nền tảng ($p, g, A$) từ Alice trước khi chuyển tiếp chúng cho Bob.
- Ta có thể đọc được toàn bộ tham số của Alice ($p, g, A, iv, encrypted$) và được phép gửi một bộ tham số giả mạo ($p', g', A'$) cho Bob.

> Goal

- Can thiệp vào bộ tham số gửi cho Bob sao cho phản hồi của Bob vô tình làm lộ khóa phiên chung (Shared Secret) dùng để mã hóa tin nhắn của Alice.

> Solution

1. Chặn tham số thật của Alice.
2. Gửi cho Bob bộ tham số giả: $p' = p$, $g' = A$ (Thay generator bằng khóa $A$ của Alice), và $A' = 0$.
3. Theo thuật toán, Bob sẽ tính khóa công khai của mình và gửi lại qua mạng:$$B = (g')^b \pmod p \Rightarrow B = A^b \pmod p$$
3. Về mặt toán học, $A^b \pmod p$ chính là Shared Secret gốc của hệ thống!Ta chỉ cần lấy thẳng giá trị $B$ mà Bob vừa gửi ra, đem băm SHA1 để tạo khóa AES và giải mã trực tiếp encrypted_A. 

```python
from pwn import *
from json import loads, dumps
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

r = remote('socket.cryptohack.org', 13373, level='error')

def send(msg):
    r.sendline(dumps(msg).encode())

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Tạo khóa AES 16-byte từ mã băm SHA1 của shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    
    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    plaintext = cipher.decrypt(bytes.fromhex(ciphertext))
    return unpad(plaintext, 16).decode('ascii')


r.recvuntil(b'Intercepted from Alice: ')
alice_params = loads(r.recvline().decode())
p = alice_params['p']
A = alice_params['A'] 

r.recvuntil(b'Intercepted from Alice: ')
alice_msg = loads(r.recvline().decode())
iv_A = alice_msg['iv']
encrypted_A = alice_msg['encrypted']

r.recvuntil(b'Bob connects to you, send him some parameters: ')
fake_params = {
    'p': p,
    'g': A,       
    'A': '0x0'    
}
send(fake_params)

r.recvuntil(b'Bob says to you: ')
bob_response = loads(r.recvline().decode())
fake_B = bob_response['B']

# Do g' = A, nên B = (g')^b mod p = A^b mod p = Shared Secret
shared_secret = int(fake_B, 16)

flag = decrypt_flag(shared_secret, iv_A, encrypted_A)
print(f"{flag}")
```
> Kết quả: 
`crypto{n07_3ph3m3r4l_3n0u6h}`

---
> #### 9. Additive

> Given

- Giao thức Diffie-Hellman (DHKE) tiêu chuẩn hoạt động dựa trên bài toán Logarit Rời Rạc trong một nhóm nhân (multiplicative group)

> Goal

- Lợi dụng sự thay đổi cấu trúc nhóm này để phá vỡ hoàn toàn độ khó của DHKE, tính toán lại khóa bí mật $a$ hoặc $b$ chỉ bằng phép toán đại số cơ bản, từ đó tìm ra khóa phiên (Shared Secret) và giải mã cờ.

> Solution

Khi chuyển giao thức sang nhóm cộng, phép lũy thừa sẽ bị giáng cấp thành phép nhân đơn thuần.
Sự biến đổi hệ quả như sau:
- Hệ chuẩn (Khó): $A = g^a \pmod p$
- Hệ cộng (Dễ): $A = g \cdot a \pmod p$
Do đó, bài toán tìm khóa bí mật $a$ không còn là Logarit Rời Rạc nữa, mà chỉ là giải phương trình tuyến tính bậc nhất. Ta dễ dàng tìm được $a$ bằng cách nhân với phần tử nghịch đảo của $g$:$$a = A \cdot g^{-1} \pmod p$$Khóa phiên chung (Shared Secret) lúc này được tính bằng:$$Key = B \cdot a \pmod p = g \cdot a \cdot b \pmod p$$

```python
from json import *
from Crypto.Util.number import inverse
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
from pwn import *

HOST = 'socket.cryptohack.org'
PORT = 13380

def cvrt(hex):
    return int(hex, 16)

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')
    
r = remote(HOST, PORT)
r.recvuntil(b'Intercepted from Alice: ')
get = loads(r.recvuntil(b'}'))
p, g, A = get['p'], get['g'], get['A']

r.recvuntil(b'Intercepted from Bob: ')
get = loads(r.recvuntil(b'}'))
B = get['B']

r.recvuntil(b'Intercepted from Alice: ')
get = loads(r.recvuntil(b'}'))
iv, encrypted = get['iv'], get['encrypted']

p, g, A, B = cvrt(p), cvrt(g), cvrt(A), cvrt(B)
a = A * inverse(g, p)
b = B * inverse(g, p)
assert (g*a*b)%p == (B*a)%p == (A*b)%p 
key = (g*a*b)%p

print(decrypt_flag(key, iv, encrypted))
```

>Kết quả: 
`crypto{cycl1c_6r0up_und3r_4dd1710n?}`

---

> #### 10. Statics Client 2

> Given

- Lỗ hổng: Mặc dù Bob kiểm tra tính hợp lệ, hệ thống lại mắc lỗi nghiêm trọng: Khóa bí mật $b$ của Bob là tĩnh (static) và không thay đổi giữa các phiên (sessions). 
- Hơn nữa, ta vẫn có quyền gửi cho Bob một module $p'$ tùy ý do ta tự chọn.
> Goal

- Tìm ra một module $p'$ "kém an toàn" (Smooth Prime) để vượt qua bước kiểm tra của Bob, khiến anh ta tái sử dụng khóa bí mật tĩnh $b$ trên $p'$ này. 
- Từ đó, giải bài toán Logarit Rời Rạc (DLP) để tìm ra $b$, tính Shared Secret trên module thật $p$ của Alice, và giải mã văn bản

> Solution

1. Tạo module giả mạo ($p'$): Sử dụng hàm toán học để sinh ra một số nguyên tố khổng lồ $p'$ sao cho $p'-1 = k!$ (giai thừa). Điều này đảm bảo $p'-1$ chỉ chứa các ước số nhỏ, biến nó thành một "Smooth Prime" hoàn hảo, đồng thời vượt qua bài kiểm tra độ lớn của Bob.(Trong code, ta đã sinh được số $p'$ dài hơn 1000 chữ số).
2. Lừa Bob tính khóa trên $p'$: Gửi cho Bob bộ tham số {"g": g, "p": fake_p, "A": A}. Bob sẽ tính toán và gửi lại $B_{fake} = g^b \pmod{p'}$.
3. Giải Pohlig-Hellman: Sử dụng hàm discrete_log của thư viện sympy để giải phương trình $g^b \equiv B_{fake} \pmod{p'}$. Do $p'$ là Smooth Prime, kết quả $b$ sẽ được tìm thấy ngay lập tức.
4. Khôi phục Flag: Dùng $b$ vừa tìm được, kết hợp với $A$ và $p$ gốc của Alice để tính khóa phiên $S = A^b \pmod p$. Cuối cùng, giải mã bằng thuật toán AES.

