# Symmetric Ciphers
---
> #### 14. Triple DES

> Given

- Hệ thống sử dụng thuật toán Triple DES (3DES) ở chế độ ECB, nhưng bọc thêm một lớp IV tĩnh (được tạo ngẫu nhiên một lần duy nhất khi server khởi động) bằng phép XOR. Công thức mã hóa: $C = E_K(P \oplus IV) \oplus IV$.
- API cho phép ta cung cấp khóa $K$ tùy ý (16-byte) để mã hóa Flag hoặc mã hóa một chuỗi văn bản bất kỳ.

> Goal

Lợi dụng điểm yếu toán học trong thuật toán sinh khóa (Key Schedule) của DES để tạo ra tính chất "tự nghịch đảo" (involution), qua đó triệt tiêu hoàn toàn ảnh hưởng của IV chưa biết và khôi phục bản rõ (Flag).

> Solution

- Khuyết điểm chí mạng của DES là tồn tại các Khóa yếu (Weak Keys). Khi sử dụng các khóa này (ví dụ: chuỗi toàn bit 0 hoặc toàn bit 1), quá trình mã hóa sẽ đảo ngược chính nó. 
- Tức là mã hóa một bản rõ hai lần liên tiếp sẽ thu lại bản rõ ban đầu: $E_K(E_K(X)) = X$.
- Đối với 3DES sử dụng khóa 16-byte (gồm hai khóa con $K_1$ và $K_2$), ta có thể tạo ra hiệu ứng tương tự bằng cách ghép hai Weak Keys lại với nhau (ví dụ: $K_1$ toàn \x00 và $K_2$ toàn \xff)

```python
import requests
from json import loads
from Crypto.Util.Padding import unpad

def encrypt(key, pt):
    key_hex = key.hex()
    pt_hex = pt.hex()
    url = f"https://aes.cryptohack.org/triple_des/encrypt/{key_hex}/{pt_hex}/"
    r = requests.get(url)
    ct = loads(r.text)['ciphertext']
    return bytes.fromhex(ct)

def encrypt_flag(key):
    key_hex = key.hex()
    url = f"https://aes.cryptohack.org/triple_des/encrypt_flag/{key_hex}/"
    r = requests.get(url)
    ct = loads(r.text)['ciphertext']
    return bytes.fromhex(ct)

keys = [
    b'\x00'*8 + b'\xff'*8,
    b'\xff'*8 + b'\x00'*8,
    b'\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01',
    b'\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00'
]


for key in keys:
    try:
        enc = encrypt_flag(key)
        
        flag = unpad(encrypt(key, enc), 8).decode()
        
        print(f"[+] Tìm thấy Weak Key hợp lệ: {key}")
        print(f"\n[🎉] FLAG: {flag}")
        break
    except Exception as e:
        print(f'[-] Khóa {key} không thành công.')
```

>Kết quả: 
`crypto{n0t_4ll_k3ys_4r3_g00d_k3ys}`

---

> #### 15. Symmetry

> Given

Hệ thống sử dụng AES ở chế độ OFB (Output Feedback). Chế độ này biến một Block Cipher (như AES) thành một Stream Cipher.

> Goal

Lợi dụng tính "đối xứng" (Symmetry) của chế độ OFB để biến hàm mã hóa (encrypt) thành hàm giải mã (decrypt) và lấy cờ.

> Solution

- Khác với ECB hay CBC, chế độ OFB không trực tiếp mã hóa bản rõ. 
- Thay vào đó, nó dùng khóa $K$ để mã hóa IV liên tục, tạo ra một dòng khóa giả ngẫu nhiên gọi là Keystream.Sau đó, bản rõ ($P$) sẽ được XOR với Keystream để tạo ra bản mã ($C$):$$C = P \oplus Keystream$$
- Vì tính chất cơ bản của phép XOR (nếu $A \oplus B = C$ thì $C \oplus B = A$), quá trình giải mã hoàn toàn y hệt quá trình mã hóa:$$P = C \oplus Keystream$$

```python
import requests
from json import loads

def encrypt(plaintext: bytes, iv: bytes):
    url = f'https://aes.cryptohack.org/symmetry/encrypt/{plaintext.hex()}/{iv.hex()}/'
    r = requests.get(url)
    return loads(r.text)['ciphertext']

def encrypt_flag():
    url = f'https://aes.cryptohack.org/symmetry/encrypt_flag/'
    r = requests.get(url)
    enc = bytes.fromhex(loads(r.text)['ciphertext'])
    return enc[:16], enc[16:]

iv, ct = encrypt_flag()


decrypted_hex = encrypt(ct, iv)

flag = bytes.fromhex(decrypted_hex).decode('ascii')
print(f"{flag}")
```

> Kết quả:
`crypto{0fb_15_5ymm37r1c4l_!!!11!}`
---

> #### 16. Bean Counter

> Given

- Chế độ CTR (Counter) hoạt động bằng cách mã hóa một bộ đếm (Counter/IV) liên tục tăng dần để tạo ra một dòng khóa giả ngẫu nhiên (Keystream). 
- Sau đó, Keystream sẽ được XOR với bản rõ (Plaintext) để tạo ra bản mã (Ciphertext). 

> Goal

- Lợi dụng việc bộ đếm bị "đóng băng", kết hợp với kỹ thuật Known Plaintext Attack (Tấn công dựa trên bản rõ đã biết) để khôi phục Keystream, từ đó giải mã toàn bộ bức ảnh chứa Flag.

> Solution

Ta tính ngược lại Keystream cực kỳ dễ dàng:$$K_{stream} = C_0 \oplus P_0$$

```python
from requests import get
from PIL import Image
from json import loads
from pwn import xor

def encrypt():
    url = 'https://aes.cryptohack.org/bean_counter/encrypt'
    r = get(url)
    enc = loads(r.text)['encrypted']
    return bytes.fromhex(enc)

first = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
ct = encrypt()

keystream = xor(first, ct[:16])
assert len(keystream) == 16
png_flag = xor(keystream, ct)

image = open('flag.png', 'wb').write(png_flag)
flag = Image.open('flag.png')
flag.show()
```
- Ta chạy xong ảnh và mở ra được flag
> Kết quả: 
`crypto{hex_bytes_beans}`
---

> #### 17. CTRIME

> Given

- Hệ thống nén dữ liệu (ở đây là zlib) bằng cách tìm các chuỗi lặp lại và thay thế chúng bằng con trỏ ngắn hơn (thuật toán LZ77). 
- Do đó, dữ liệu có nhiều phần lặp lại sẽ có kích thước nén nhỏ hơn.
- Dữ kiện: Server ghép đoạn plaintext ta gửi vào cùng với FLAG, nén chúng lại bằng zlib.compress, rồi mới mã hóa bằng AES-CTR. AES-CTR là một Stream Cipher, nó bảo toàn nguyên vẹn độ dài của bản rõ sau khi mã hóa.

> Goal

Lợi dụng sự thay đổi kích thước của bản mã (Ciphertext) để đoán từng ký tự của Flag. Đây là dạng tấn công Side-Channel (Kênh kề) qua độ dài dữ liệu nén.

> Solution

Nếu ta gửi lên một đoạn plaintext chứa phần đầu của Flag cộng thêm 1 ký tự đoán thử (ví dụ: crypto{a), zlib sẽ quét thấy chuỗi này xuất hiện lần thứ hai ở phần FLAG thật bị nối phía sau.

- Nếu ký tự đoán SAI: Chuỗi lặp lại bị ngắt quãng, độ dài nén sẽ lớn hơn.

- Nếu ký tự đoán ĐÚNG: Chuỗi lặp lại dài hơn, zlib nén tối ưu hơn, dẫn đến độ dài bản mã ngắn nhất.

```python
import requests
from json import loads
import string

def encrypt(pt_bytes):
    pt_hex = pt_bytes.hex()
    url = f'https://aes.cryptohack.org/ctrime/encrypt/{pt_hex}/'
    r = requests.get(url)
    ct = loads(r.text)['ciphertext']
    return len(ct) 

FLAG = b'crypto{'
chars = string.ascii_letters + string.digits + '_}'

while True:
    min_len = 9999
    best_char = ''
    
    for char in chars:
        guess = FLAG + char.encode()
        pt = guess * 2 
        
        ct_len = encrypt(pt)
        
        if ct_len < min_len:
            min_len = ct_len
            best_char = char
    FLAG += best_char.encode()
    print(f"{FLAG.decode()}")
    
    if best_char == '}':
        break
```
> Kết quả:
`crypto{CRIME_571ll_p4y5}`

---

> #### 18. Logon Zero

> Given

-  Chế độ AES-CFB8 (Cipher Feedback 8-bit) có một lỗ hổng toán học chết người khi khởi tạo. Nếu đầu vào toàn là byte \x00, có một xác suất $1/256$ mà toàn bộ quá trình mã hóa/giải mã sẽ sinh ra đầu ra cũng toàn là byte \x00.
- Server cung cấp 3 API: reset_connection (tạo lại khóa/IV mới), reset_password (nhận một token và giải mã nó bằng CFB8 để làm mật khẩu mới), và authenticate (kiểm tra mật khẩu).

> Goal 

- Lợi dụng điểm yếu của CFB8 để ép máy chủ đổi mật khẩu của admin thành một chuỗi toàn số $0$, sau đó đăng nhập bằng mật khẩu toàn số $0$ đó để lấy Flag.

> Solution

1. Gửi token toàn \x00.Đăng nhập thử với mật khẩu toàn \x00.
2. Nếu sai $\rightarrow$ Mật khẩu sinh ra bị rác $\rightarrow$ 
3. Gọi reset_connection để thử lại với cấu hình mới.
4. Lặp lại liên tục (Brute-force) cho đến khi trúng được tỉ lệ $1/256$

```python
from pwn import *
from json import dumps, loads

HOST = 'socket.cryptohack.org'
PORT = 13399

def send_json(msg):
    r.sendline(dumps(msg).encode())

context.log_level = 'error'

r = remote(HOST, PORT)
r.recvline() 

exploit_token = b'\x00' * 28 

expected_password = "" 

attempts = 0

while True:
    attempts += 1
    
    send_json({'option': 'reset_password', 'token': exploit_token.hex()})
    r.recvline()

    send_json({'option': 'authenticate', 'password': expected_password})
    response_data = r.recvline()
    
    if not response_data:
        continue
        
    response = loads(response_data)['msg']
    
    if 'Welcome admin, flag: ' in response:
        break
    send_json({'option': 'reset_connection'})
    r.recvline()

r.close()
```
> Kết quả: 
`crypto{Zerologon_Windows_CVE-2020-1472}`

---

> #### 19. Stream of Consciousness

> Given

Chế độ CTR (Counter) biến Block Cipher thành Stream Cipher bằng cách mã hóa bộ đếm để tạo ra Keystream, sau đó XOR với Plaintext.

> Goal 

- Thực hiện cuộc tấn công Many-Time Pad (Keystream Reuse). Khi Keystream bị sử dụng lại, nếu ta XOR hai bản mã với nhau, Keystream sẽ tự triệt tiêu, để lại kết quả là XOR của hai bản rõ gốc:
$$C_1 \oplus C_2 = (P_1 \oplus K) \oplus (P_2 \oplus K) = P_1 \oplus P_2$$
- Nhiệm vụ là từ $P_1 \oplus P_2$ này, dùng một phần bản rõ đã biết (Known Plaintext - như chữ crypto{) để khôi phục các văn bản còn lại.

> Solution

- Vì ta biết Flag bắt đầu bằng crypto{, nếu một trong hai bản mã trong tổ hợp là Flag, thì kết quả $C_1 \oplus C_2 \oplus \text{`crypto\{`}$ sẽ nhả ra phần đầu của bản rõ kia (thường là một từ tiếng Anh có nghĩa).
- Tuy nhiên, thay vì đoán mò từng chữ bằng mắt thường (Crib Drag), ta có một chiến thuật mạnh hơn nhiều:Ta nhận thấy các bản rõ đều là văn bản tiếng Anh (chỉ chứa chữ cái và dấu câu). 
- Nếu ta dùng một đoạn Keystream dự đoán đi XOR với toàn bộ 22 bản mã, Keystream ĐÚNG sẽ khiến tất cả 22 kết quả giải mã đều nằm trong dải ký tự có thể in được (printable characters).
```python
from pwn import xor
from itertools import combinations
import string

# Danh sách stream của bạn (đã được dọn dẹp)
stream = ['be9065d98ec30981b8b90bfb41', 'b39063c6e7b41691f4ba5efa16a35056093b7403', 'b08b73c6e7b41290f9ba12a917ab49191337394488a6', 'b5977295ddb90c99f3bf10ee5ead4912411f704190e1d71846e3', '92976e96dafb1a93abaf4bbe0cff131b3e202a58c9bbe64c01c5fb6061d51c9d', 'a68d76928ef54196f9a50af05ebf4a130d3e395994e1ca5d44fbf43a22c118818347', 'b8913785cffa468cb8b41ba90aa35518413d6c59d0a8db0840baf4207682118ec70b7fdc10e71b173974c60a', 'b8c5648ecff80dd8f4b90dec5ea95113132b6d4595e6de5d55f4f974388e04c0800c6edc11e918582970c14f71', 'a58d6583cbb40397e1a55efb0ba2491f0f35350d8ce4d8045df4fa7437955088881b69990aac552b2e63db4b256ec957', 'b096378fc8b428d8f0b71aa91fa25e56163b6a45dcfcd65d56ffbd3d38c10488824968951ee801596b5882473e688f02f8', 'bf8a3bc6e7b30d94b8b111a917a207020e725d4290e4c05d55f4f97422841c8cc7017f8e59f3010a2a78c54c2b26c703ad', 'b98a60c6dee60e8dfcf61fe71aec4f171122600d94ed9e1158baff31769618858949729959e7100c3831cf5d7f68c702bcb8', 'a68d6ec6cafb418cf0b307a919a307190f72694c95e6cd145afdbd35388550829200769810ee12582a7dce042b6ecd56adf065ddbe', 'b8c5648ecff80dd4b89f59e512ec4b19123739488aedcb0440f2f43a31c11986c7017fdc1def100b2536d6043c69c513f9fb69dbea4e', 'a58d72c6daf1138af1b412ec5eb84f1f0f3539448fa8cd1555eebd203e845090861a6edc1ae11b5f3f31c0417f72c704b7b967cdf5403ae08481cc770641d19122ab01', 'a68a628acab428d8f0b708ec5eae421a08376f4898a8cd1551f4bd203e8004c0ae4979930cec11583974c3473726db03baf128dce4102cf1d7c8d762065bcb933fb4463501a4e02b0a', 'a180658ecfe412d8f0b35ee11fbf071b08216a4898a8cd1551bae92637881ec086077edc10f3551a2a72c9043d7f8818b6ee2698d60136ed8485d7764313d68b3bb1433d14b9e62a5b1f', 'b8c27ac6dbfa0999e8a607a55e85071204217c5f8aed991440b6bd203e845086861c76885ef35515227fc7087f64dd02f9d02fd5a11536f1c598c87d0652d29276ac473155beee2850123af77a47ca7588bd5f', 'bd8a618382b4118af7b41feb12b51856353a7c54dcecd61313eebd3f388e07c08f066ddc1df210193968824d2b26c105f5b960d7f64030ecc981d46d4747d79031f6017a55b9e720157f6cfa715edf7584b615e96e659520c714359a1a', 'b58a7b8ad7b41691f4ba5efd16a5491d4126714c88a8f05a59baf1313797198e80497bdc0ae516172575824c2a75ca17b7fd28d9ef0478edcc89cc24525bdb8c33be402610edc665584b69eb3f58cf2780b408e96f68dc25cd46249c51614cccfca866d8', 'a58d7295cbb40997eaa51bfa52ec531e0821394e9dfacb1455fdf8747bc1188f904953dc15ef140c237482492675cd1abfb961d6a11430f0d7c8db655441d79f31bd0f7955b9e7204c1968fa3f4ad639c5b018ba362d9e39d74619d447295ad2ffe66f932603fe7a2af2f968e471b7c5675759d26ec1ce', 'a68d76928ef54194f7a25ee618ec531e083c7e5edcfcd11c40bae93c338f5093820c77991da001176b7cc7042c69881bb8eb7edded0c37ecd7c8d96a4213cb9037ac5b351ca3ee27595b36bf774acc30c5ba14aa6260996cca08239d532f52d8faa56098244aac3b37f3bc3cf87cf2dc2f5f50d4748fa92da5730f18b904a1cbf57534ed4393f668ccd755fb360203d80434c04e4b481cddff7780ad9afcf6']
flag_prefix = b'crypto{'
stream_bytes = [bytes.fromhex(s) for s in stream]


# Thử từng cặp
for c1, c2 in combinations(stream_bytes, 2):
    min_len = min(len(c1), len(c2), len(flag_prefix))
    
    diff = xor(c1[:min_len], c2[:min_len])
    result = xor(diff, flag_prefix[:min_len])
    
    if all(chr(b) in string.printable for b in result):
        print(f"Manh mối tiềm năng: {result}")
```
> Kết quả:
`crypto{k3y57r34m_r3u53_15_f474l}`

--- 

> #### 20. Dancing Queen
### Given
- Một challenge tên “Dancing Queen”.
- Tác giả tự triển khai (custom) thuật toán ChaCha20 thay vì dùng chuẩn.
- Có 2 file được cung cấp: chacha20.py (code triển khai thuật toán), output.txt (ciphertext / dữ liệu đã mã hóa)
### Goal
- Phân tích implementation ChaCha20 tùy chỉnh để tìm ra sai sót hoặc điểm yếu.
- Từ đó giải mã output.txt và khôi phục plaintext.
- Thu được flag dạng crypto{...}.
### Solution
```python

 
from os import urandom
from Crypto.Util.number import *
 
FLAG = b'crypto{?????????????????????????????}'
 
 
def bytes_to_words(b):
    return [int.from_bytes(b[i:i + 4], 'little') for i in range(0, len(b), 4)]
 
 
def rotate(x, n):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)
 
def rotate_reverse(x, n):
    return ((x << (32 - n)) & 0xffffffff) | ((x >> n) & 0xffffffff)
 
def word(x):
    return x % (2 ** 32)
 
 
def words_to_bytes(w):
    return b''.join([i.to_bytes(4, 'little') for i in w])
 
 
def xor(a, b):
    return b''.join([bytes([x ^ y]) for x, y in zip(a, b)])
 
 
class ChaCha20:
    def __init__(self):
        self._state = []
 
    def _inner_block(self, state):
        self._quarter_round(state, 0, 4, 8, 12)
        self._quarter_round(state, 1, 5, 9, 13)
        self._quarter_round(state, 2, 6, 10, 14)
        self._quarter_round(state, 3, 7, 11, 15)
        self._quarter_round(state, 0, 5, 10, 15)
        self._quarter_round(state, 1, 6, 11, 12)
        self._quarter_round(state, 2, 7, 8, 13)
        self._quarter_round(state, 3, 4, 9, 14)
 
    def _quarter_round(self, x, a, b, c, d):
        x[a] = word(x[a] + x[b]);
        x[d] ^= x[a];
        x[d] = rotate(x[d], 16)
        x[c] = word(x[c] + x[d]);
        x[b] ^= x[c];
        x[b] = rotate(x[b], 12)
        x[a] = word(x[a] + x[b]);
        x[d] ^= x[a];
        x[d] = rotate(x[d], 8)
        x[c] = word(x[c] + x[d]);
        x[b] ^= x[c];
        x[b] = rotate(x[b], 7)
 
    def _inner_block_revese(self, state):
        self._quarter_round_revese(state, 3, 4, 9, 14)
        self._quarter_round_revese(state, 2, 7, 8, 13)
        self._quarter_round_revese(state, 1, 6, 11, 12)
        self._quarter_round_revese(state, 0, 5, 10, 15)
        self._quarter_round_revese(state, 3, 7, 11, 15)
        self._quarter_round_revese(state, 2, 6, 10, 14)
        self._quarter_round_revese(state, 1, 5, 9, 13)
        self._quarter_round_revese(state, 0, 4, 8, 12)
 
    def _quarter_round_revese(self, x, a, b, c, d):
        x[b] = rotate_reverse(x[b], 7)
        x[b] ^= x[c]
        x[c] = word(x[c] - x[d])
        x[d] = rotate_reverse(x[d], 8)
        x[d] ^= x[a]
        x[a] = word(x[a] - x[b])
        x[b] = rotate_reverse(x[b], 12)
        x[b] ^= x[c]
        x[c] = word(x[c] - x[d])
        x[d] = rotate_reverse(x[d], 16)
        x[d] ^= x[a]
        x[a] = word(x[a] - x[b])
 
    def _setup_state(self, key, iv):
        self._state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
        self._state.extend(bytes_to_words(key))
        self._state.append(self._counter)
        self._state.extend(bytes_to_words(iv))
 
    def decrypt(self, c, key, iv):
        return self.encrypt(c, key, iv)
 
    def encrypt(self, m, key, iv):
        c = b''
        self._counter = 1
 
        for i in range(0, len(m), 64):
            self._setup_state(key, iv)
            for j in range(10):
                self._inner_block(self._state)
            c += xor(m[i:i + 64], words_to_bytes(self._state))
 
            self._counter += 1
 
        return c
 
    def state_reverse(self, msg, cipher):
        state = []
        for i in range(64):
            state.append(msg[i] ^ cipher[i])
        self._state = []
        self._state.extend(bytes_to_words(state))
        # print(self._state)
        for i in range(10):
            self._inner_block_revese(self._state)
            # self._inner_block(self._state)
 
 
        for i in range(16):
            print(hex(self._state[i]) + " ", end="")
        print()
        print(hex(bytes_to_long(words_to_bytes(self._state[4:12]))))
if __name__ == '__main__':
    msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'
    iv1 = 'e42758d6d218013ea63e3c49'
    iv1=bytes.fromhex(iv1)
    iv2 = 'a99f9a7d097daabd2aa2a235'
    iv2=bytes.fromhex(iv2)
    key = '39fd1410fef6485bf3068ea0fb3a8ff6385b4483bc1f321cea4f15cc1c43496c'
    key=bytes.fromhex(key)
    msg_enc = 'f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f'
    flag_enc = 'b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732'
    c = ChaCha20()
    c.state_reverse(msg[:64],bytes.fromhex(msg_enc)[:64])
    msg_enc = c.decrypt(bytes.fromhex(msg_enc), key, iv1)
    flag_enc = c.decrypt(bytes.fromhex(flag_enc), key, iv2)
    print(f"msg_enc = '{msg_enc}'")
    print(f"flag_enc = '{flag_enc}'")
```
> Kết quả:
`crypto{M1x1n6_r0und5_4r3_1nv3r71bl3!}`
