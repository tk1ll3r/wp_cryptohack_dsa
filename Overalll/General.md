# **General**
## **1. ASCII**

### Given
ASCII là một chuẩn mã hóa 7 bit cho phép biểu diễn văn bản bằng các số nguyên từ 0 đến 127.

### Goal 

Sử dụng mảng số nguyên bên dưới, hãy chuyển đổi các số thành các ký tự ASCII tương ứng để thu được một cờ: (`[99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]`).

### Solution

Bài này ta sử dụng hàm `chr()` để chuyển đổi số thứ tự ASCII thành ký tự

```python
ascii_list = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]

s = ''.join(chr(x) for x in ascii_list)
print(s)

```

Chạy code ra được flag `cypto{ASCII_pr1nt4bl3}`


## **2. HEX**

### Given
- Hệ thập lục phân có thể được sử dụng theo cách này để biểu diễn các chuỗi ASCII. 
- Đầu tiên, mỗi chữ cái được chuyển đổi thành một số thứ tự theo bảng ASCII (như trong thử thách trước). 
- Sau đó, các số thập phân được chuyển đổi thành số cơ số 16, hay còn gọi là hệ thập lục phân. Các số này có thể được kết hợp với nhau thành một chuỗi thập lục phân dài.

### Goal 

- Một cờ được mã hóa dưới dạng chuỗi thập lục phân.
`63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d`
-  Giải mã chuỗi này trở lại thành byte để lấy cờ.

### Solution

Bài này ta sử dụng hàm `bytes.fromhex()` hàm này có thể được sử dụng để chuyển đổi hệ thập lục phân sang byte
```python
hex_string = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
flag = bytes.fromhex(hex_string).decode()
print(flag)

```

### Chạy code ra được flag: 

`crypto{You_will_be_working_with_hex_strings_a_lot}`


## **3. BASE64**

### Given
- Một lược đồ mã hóa phổ biến khác là Base64, cho phép chúng ta biểu diễn dữ liệu nhị phân dưới dạng chuỗi ASCII bằng bảng chữ cái gồm 64 ký tự.
- Một ký tự của chuỗi Base64 mã hóa 6 chữ số nhị phân (bit), và do đó 4 ký tự Base64 mã hóa ba byte 8 bit.

### Goal
- Hãy lấy chuỗi thập lục phân bên dưới, giải mã nó thành byte và sau đó mã hóa nó thành Base64.
`72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf`

### Solution
- Bài này ta sử dụng `base64.b64encode()` trong Python để mã hóa chuỗi byte từ hex sang Base64.

```python
import base64

hex_string = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
raw_bytes = bytes.fromhex(hex_string)
encoded = base64.b64encode(raw_bytes)

print(encoded.decode())
```

### Kết quả
`crypto/Base+64+Encoding+is+Web+Safe/`



## **4. Bytes and Big Integers**

### Given
- Các hệ mật mã như RSA hoạt động trên các con số, nhưng thông điệp lại được tạo thành từ các ký tự.
- Để chuyển đổi thông điệp thành các con số để có thể áp dụng các phép toán, cách phổ biến nhất là lấy các byte thứ tự của thông điệp, chuyển đổi chúng thành hệ thập lục phân, rồi ghép nối lại.
- Kết quả có thể được hiểu là một số thập lục phân/cơ số 16, và cũng có thể được biểu diễn trong hệ thập phân/cơ số 10.

### Goal
- Chuyển số nguyên hệ 10 thành bytes, rồi diễn giải bytes đó thành ký tự ASCII/text.
`11515195063862318899931685488813747395775516287289682636499965282714637259206269`

### Solution
```python
n = 11515195063862318899931685488813747395775516287289682636499965282714637259206269

b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
print(b)
print(b.decode())
```

### Kết quả
`crypto{3nc0d1n6_4ll_7h3_w4y_d0wn}`



## **5. Encoding Challenge**

### Given
- Đây là một bài **interactive challenge**.
- Server sẽ gửi về dữ liệu ở dạng JSON, gồm:
  - `type`: kiểu mã hóa
  - `encoded`: dữ liệu đã mã hóa
- Nhiệm vụ của mình là giải mã giá trị `encoded` theo đúng kiểu `type`, rồi gửi lại cho server đúng dạng.

### Goal
- Kết nối tới server của challenge.
- Nhận dữ liệu mã hóa mà server gửi về.
- Xác định kiểu mã hóa qua trường `type`.
- Giải mã trường `encoded` về chuỗi gốc.
- Gửi lại đáp án đúng cho server dưới dạng JSON.
- Lặp lại nhiều lần cho đến khi server trả về flag.

### Solution
```python
import socket
import json
import base64
import codecs

HOST = "socket.cryptohack.org"
PORT = 13377


def decode_data(data):
	t = data["type"]
	e = data["encoded"]

	if t == "base64":
		return base64.b64decode(e).decode()

	elif t == "hex":
		return bytes.fromhex(e).decode()

	elif t == "rot13":
		return codecs.decode(e, "rot_13")

	elif t == "bigint":
		n = int(e, 16)
		b = n.to_bytes((n.bit_length() + 7) // 8, "big")
		return b.decode()

	elif t == "utf-8":
		return "".join(chr(x) for x in e)

	else:
		raise ValueError(f"Unknown type: {t}")


with socket.create_connection((HOST, PORT)) as s:
	f = s.makefile("rw")

	while True:
		line = f.readline()
		if not line:
			break

		data = json.loads(line)
		print("Received:", data)

		if "flag" in data:
			print("FLAG:", data["flag"])
			break

		decoded = decode_data(data)
		response = {"decoded": decoded}

		f.write(json.dumps(response) + "\n")
		f.flush()
```

### Kết quả
`crypto{3nc0d3_d3c0d3_3nc0d3}`



## **6. XOR Starter**
### Given
- XOR (^) là phép toán bitwise: trả về 0 nếu hai bit giống nhau, 1 nếu khác nhau.

- Chuỗi đầu vào: `label`

- Mỗi ký tự trong chuỗi sẽ được XOR với số nguyên 13.

### Goal
- XOR từng ký tự của chuỗi `label` với 13, chuyển kết quả ngược lại thành chuỗi, rồi submit flag theo định dạng `crypto{new_string}`.

### Solution
- **Ý tưởng:** Với mỗi ký tự c trong chuỗi, ta thực hiện: ord(c) ^ 13, sau đó dùng `chr()` để chuyển ngược về ký tự.
    ```python
    label = "label"
    result = ''.join(chr(ord(c) ^ 13) for c in label)
    print(f"crypto{{{result}}}")
    ```

- **Trace từng bước:**

<div align="center">

| Ký tự | ord(c) | ord(c) ^ 13 | Kết quả |
| :---: | :---: | :---: | :---: |
| l | 108 | 97 | a |
| a | 97 | 108 | l |
| b | 98 | 111 | o |
| e | 101 | 104 | h |
| l | 108 | 97 | a |

</div>

- Nếu dùng `pwntools`, có thể rút gọn thành một dòng:
    ```python
    from pwn import xor
    print(xor(b"label", 13).decode())
    ```

### Kết quả
- `label` XOR `13` = "aloha"

`crypto{aloha}`


## **7. XOR Properties**
### Given
- Bài cung cấp 4 dòng dữ liệu dưới dạng `hex`:
    ```python
    KEY1="a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
    KEY2^KEY1="37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
    KEY2^KEY3="c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
    FLAG^KEY1^KEY3^KEY2="04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"
    ```

- Bốn tính chất của `XOR`:
    ```text
    - Commutative: A ⊕ B = B ⊕ A
    - Associative: A ⊕ (B ⊕ C) = (A ⊕ B) ⊕ C
    - Identity: A ⊕ 0 = A
    - Self-Inverse: A ⊕ A = 0
    ```

### Goal
- Sử dụng các tính chất của XOR để lần ngược lại chuỗi mã hóa, khôi phục FLAG từ biểu thức `FLAG ^ KEY1 ^ KEY3 ^ KEY2`.

### Solution
- **Bước 1 — Tìm KEY2**

    Ta có: `KEY2 ^ KEY1 = 37dcb2...`

    XOR cả hai vế với `KEY1`:
    $$KEY2⊕KEY1⊕KEY1=KEY2⊕0=KEY2$$

- **Bước 2 — Tìm KEY3**

    Ta có: `KEY2 ^ KEY3 = c15457...`

    XOR cả hai vế với `KEY2` vừa tìm được:
    $$KEY2⊕KEY3⊕KEY2=KEY3$$

- **Bước 3 — Tìm FLAG**

    Ta có: `FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee98...`

    XOR cả hai vế với KEY1, KEY3, KEY2:
    $$FLAG⊕KEY1⊕KEY3⊕KEY2⊕KEY1⊕KEY3⊕KEY2=FLAG$$

    ```python
    KEY1 = bytes.fromhex("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313")
    K2xK1 = bytes.fromhex("37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e")
    K2xK3 = bytes.fromhex("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1")
    FxK1xK3xK2 = bytes.fromhex("04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf")

    KEY2 = bytes(a ^ b for a, b in zip(K2xK1, KEY1))
    KEY3 = bytes(a ^ b for a, b in zip(K2xK3, KEY2))
    FLAG = bytes(a ^ b ^ c ^ d for a, b, c, d in zip(FxK1xK3xK2, KEY1, KEY3, KEY2))

    print(FLAG.decode())
    ```

### Kết quả
`crypto{x0r_i5_ass0c1at1v3}`


## **8. Favourite byte**

### Given
- Đề bài cung cấp một chuỗi hex:
    ```
    73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d`
    ```

- Biết rằng dữ liệu đã bị XOR với một `single-byte key`.

### Goal
- Tìm byte bí mật đó và giải mã chuỗi hex để lấy lại flag.

### Solution
- **Ý tưởng:** Brute-force toàn bộ 256 khả năng

- Vì key chỉ là một byte duy nhất nên giá trị của nó nằm trong khoảng `0x00` đến `0xff` *(tức là chỉ có 256 khả năng)*.

- Ta sẽ lần lượt XOR ciphertext với từng giá trị từ 0 đến 255, rồi kiểm tra xem kết quả có bắt đầu bằng `crypto{` không.

    ```python
    ciphertext = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")

    for key in range(256):
        plaintext = bytes(b ^ key for b in ciphertext)
        try:
            decoded = plaintext.decode('ascii')
            if decoded.startswith("crypto{"):
                print(decoded)
        except:
            pass
    ```

### Kết quả
`crypto{0x10_15_my_f4v0ur173_by7e}`


## **9. You either know, XOR you don't**

### Given
- Chuỗi hex đã được mã hóa:
    ```
    0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104
    ```

- Flag được mã hóa bằng một `secret key` — không biết độ dài hay nội dung của `key`.

### Goal
- Tìm `secret key` và giải mã ciphertext để lấy flag.

### Solution
- **Ý tưởng:** Known Plaintext Attack với tiền tố `crypto{`

    - Vì ta biết flag luôn bắt đầu bằng `crypto{` *(7 ký tự)*, đây chính là **known plaintext**. Do đó, ta dùng tính chất `Self-Inverse` của XOR
    
    => Khi XOR phần đầu của ciphertext với `crypto{` sẽ cho ra 7 byte đầu tiên của key:
    $$FLAG⊕KEY=CIPHER⟹KEY=CIPHER⊕FLAG$$

    ```python
    # Bước 0: Decode hex sang bytes
    ciphertext = bytes.fromhex("0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104")
    known = b"crypto{"

    # Bước 1: XOR phần đầu ciphertext với known plaintext để lấy một phần key
    key_partial = bytes(c ^ p for c, p in zip(ciphertext, known))
    ##### → b'myXORke' -> suy đoán key đầy đủ là b'myXORkey'

    # Bước 2: Lặp key để phủ toàn bộ độ dài ciphertext
    key = b"myXORkey"
    full_key = (key * ((len(ciphertext) // len(key)) + 1))[:len(ciphertext)]

    # Bước 3: Giải mã bằng cách XOR ciphertext với key đã mở rộng
    plaintext = bytes(c ^ k for c, k in zip(ciphertext, full_key))
    print(plaintext.decode())
    ```

### Kết quả
`crypto{1f_y0u_Kn0w_En0uGH_y0u_Kn0w_1t_4ll}`


## **10. Lemur XOR**

### Given
- Hai file ảnh bị mã hóa: `flag.png` và `lemur.png`. Hiện tại khi nhìn vào, cả hai ảnh chỉ hiển thị nhiễu hạt (noise).

- Hai ảnh này đã được ẩn đi bằng cách XOR với cùng một `secret key`.

- Gợi ý: Thực hiện phép toán XOR trực tiếp giữa các byte màu RGB của hai hình ảnh với nhau.

### Goal
- Khai thác lỗ hổng tái sử dụng khóa (key reuse/many-time pad) để loại bỏ khóa bí mật $K$, từ đó khôi phục lại hình ảnh ban đầu và tìm ra flag.

### Solution
- Sử dụng tính chất toán học của phép XOR:
    - Identity: $$A ⊕ 0 = A$$
    - Self-Inverse: $$A ⊕ A = 0$$

- **Giả sử:**
    - $M_1$ là mảng pixel của `flag.png`.
    - $M_2$ là mảng pixel của `lemur.png`.
    - $K$ là Secret Key.

- Theo đề bài, hai ảnh bị nhiễu mà chúng ta đang có chính là các **Ciphertext**:
    $$C_1 = M_1 \oplus K$$
    $$C_2 = M_2 \oplus K$$

- Vì cả hai ảnh đều bị XOR bởi cùng một khóa $K$, ta có thể thực hiện phép toán XOR giữa hai bản mã này với nhau. Điều này sẽ giúp triệt tiêu khóa $K$:
    $$C_1 \oplus C_2 = (M_1 \oplus K) \oplus (M_2 \oplus K)$$
    $$C_1 \oplus C_2 = M_1 \oplus M_2 \oplus (K \oplus K)$$
    $$C_1 \oplus C_2 = M_1 \oplus M_2 \oplus 0$$
    $$C_1 \oplus C_2 = M_1 \oplus M_2$$

    ```python
    from PIL import Image
    import numpy as np
    import os

    # Bước 1: Thiết lập đường dẫn file chính xác (tránh lỗi FileNotFound)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_flag = os.path.join(current_dir, "flag.png")
    file_path_lemur = os.path.join(current_dir, "lemur.png")

    # Bước 2: Tải dữ liệu ảnh từ bộ nhớ
    img_flag = Image.open(file_path_flag)
    img_lemur = Image.open(file_path_lemur)

    # Bước 3: Chuyển đổi ảnh sang dạng mảng NumPy để tính toán
    arr_flag = np.array(img_flag)
    arr_lemur = np.array(img_lemur)

    # Bước 4: Thực hiện phép toán bitwise XOR giữa hai lớp ảnh
    result_arr = np.bitwise_xor(arr_flag, arr_lemur)

    # Bước 5: Chuyển đổi mảng kết quả ngược lại về định dạng ảnh
    result_img = Image.fromarray(result_arr)

    # Bước 6: Lưu tệp và hiển thị kết quả "decrypted_flag.png"
    result_img.save(os.path.join(current_dir, "decrypted_flag.png"))
    result_img.show()
    ```

### Kết quả

`crypto{XORly_n0t!}`


## **11. Greatest Common Divisor**

### Given
- Greatest Common Divisor (GCD) là số nguyên dương lớn nhất có thể chia hết cho cả hai số a và b.
- Coprime (nguyên tố cùng nhau): Hai số $a$ và $b$ được gọi là nguyên tố cùng nhau nếu `gcd(a, b) = 1`.

### Goal
- Tìm kết quả ước chung lớn nhất giữa 66528 và 52920 (`gcd(66528,52920)`).

### Solution
- Ở bài này mình sử dụng thuật toán Euclid:

$$\gcd(a, b) = \gcd(b, a \bmod b)$$

- Mình sử dụng vòng lặp cho tới khi b = 0, trả về a là UCLN.

```python
def gcd(a, b):
    if a < b:
        a, b = b, a  # luôn cho a > b

    while b != 0:
        a, b = b, a % b  # sử dụng thuật toán Euclid
    return a  # a chính là UCLN


print(gcd(66528, 52920))
```

### Kết quả
`1512`




## **12. Extended GCD**

### Given
- Bài toán giới thiệu Thuật toán Euclid mở rộng (Extended Euclidean Algorithm). Nó không chỉ tìm Ước chung lớn nhất (GCD) như thuật toán thường, mà còn tìm ra hai số nguyên $u, v$ thỏa mãn Đồng nhất thức Bézout:

$$a \cdot u + b \cdot v = \gcd(a, b)$$

### Goal
- Dùng Euclid mở rộng để tính ra hai hệ số $u$ và $v$ của phương trình:

$$26513 \cdot u + 32321 \cdot v = 1$$

- So sánh giá trị của $u$ và $v$, tìm ra con số nhỏ hơn để nộp.

### Solution
- Ở bài toán này, chúng ta cần biểu diễn phương trình toán học ở mỗi bước.
- Tại mỗi bước ta biểu diễn được hai số `a` và `b` theo 2 số ban đầu.
- Lưu lại từ bước trước sang bước sau.

```python
def extended_gcd(a, b):
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1

    while b != 0:
        q = a // b
        a, b = b, a % b

        x0, x1 = x1, x0 - q * x1  # Cập nhật hệ số x (tương ứng với u)
        y0, y1 = y1, y0 - q * y1  # Cập nhật hệ số y (tương ứng với v)

    return a, x0, y0  # a là gcd(p, q)


p = 26513
q = 32321
gcd_val, u, v = extended_gcd(p, q)

flag = min(u, v)
print(flag)
```

### Kết quả
`-8404`




## **13. Modular Arithmetic 1**

### Given
- Đề bài giới thiệu Số học Module (Modular Arithmetic).
- Định nghĩa: Ký hiệu $a \equiv b \pmod m$ hiểu đơn giản là khi lấy số $a$ chia cho số $m$, ta được phần dư là $b$.

### Goal
- Tìm số dư $x$ của phép tính $11 \bmod 6$.
- Tìm số dư $y$ của phép tính $8146798528947 \bmod 17$.
- Lấy số nhỏ hơn giữa $x$ và $y$.

### Solution
```python
x = 11 % 6
y = 8146798528947 % 17
# tính x, y bằng cách lấy phần dư

flag = min(x, y)
```

### Kết quả
`4`



## **14. Modular Arithmetic 2**

### Given
- Đề bài giới thiệu về Trường hữu hạn (Finite Field).
- Chúng ta cần sử dụng định lý nhỏ Fermat để làm bài này.
- Định lý nhỏ Fermat phát biểu rằng: Nếu $p$ là số nguyên tố, thì với mọi số nguyên $a$ (không chia hết cho $p$), ta luôn có:

$$a^{p-1} \equiv 1 \pmod p$$

### Goal
- Tính giá trị của phép toán:

$$273246787654^{65536} \pmod{65537}$$

### Solution
Đề bài cho:
- Số modulo $p = 65537$ (đây là một số nguyên tố nổi tiếng).
- Số mũ là $65536$, chính xác bằng $p - 1$.
- Cơ số $a = 273246787654$ rất lớn.

Áp dụng định lý Fermat nhỏ ta được kết quả bằng 1.

- Chúng ta có thể dùng Python, tính lũy thừa modulo bằng hàm `pow(base, exp, mod)`.

```python
a = 273246787654
p = 65537

# Dùng hàm pow() để tính lũy thừa modulo
result = pow(a, p - 1, p)

print(result)
```

### Kết quả
`1`



## **15. Modular Inverting**

### Given
- Đề bài giới thiệu khái niệm Nghịch đảo nhân (Multiplicative Inverse) trong trường hữu hạn $F_p$.
- Định nghĩa: Phần tử $d$ được gọi là nghịch đảo của $g$ trong modulo $p$ nếu tích của chúng chia cho $p$ dư 1. Ký hiệu toán học:

$$g \cdot d \equiv 1 \pmod p$$

Người ta thường ký hiệu $d$ là $g^{-1}$.

### Goal
- Tìm giá trị $d = 3^{-1} \pmod{13}$.
- Tức là tìm số nguyên $d$ sao cho: $3 \cdot d \equiv 1 \pmod{13}$.

### Solution
- Phương trình Bézout mà chúng ta đã chứng minh ở bài trước:

$$a \cdot x + m \cdot y = \gcd(a, m)$$

- Áp dụng vào bài này với $a = 3$ và $m = 13$ (vì 13 là số nguyên tố nên $\gcd(3, 13) = 1$):

$$3 \cdot x + 13 \cdot y = 1$$

- Nếu ta lấy modulo 13 cho cả hai vế (làm cho cụm $13 \cdot y$ bằng 0):

$$3 \cdot x \equiv 1 \pmod{13}$$

- Kết luận: Hệ số $x$ được sinh ra từ thuật toán Extended GCD chính là phần tử nghịch đảo $d$ mà chúng ta cần tìm.

```python
def egcd(a, b):
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    # Trả về x0 - hệ số đi kèm với a ban đầu
    return x0


m = 13
x0 = egcd(3, m)
# tính ra hệ số x0

inverse = x0 % m  # số x0 cần phải dương trong khoảng [0, m-1]
print(inverse)
```

### Kết quả
`9`

## **16. Data Formats**
### 1.Given 
![alt text](assets/general/16_1.png)
![alt text](assets/general/16_2.png)
![alt text](assets/general/16_3.png)
### 2.Goal
* **Mục tiêu:** Trích xuất giá trị số nguyên thập phân của số mũ bí mật (**private key $d$**) từ một file định dạng **.pem**.
* **Định dạng PEM:** Là một dạng "bao bì" (container) chứa dữ liệu đã được mã hóa **Base64**. Dữ liệu bên trong Base64 tuân theo cấu trúc **ASN.1** và được mã hóa bằng chuẩn **DER**.
* **Tệp tin cung cấp:** `privacy_enhanced_mail.pem` chứa một khóa RSA Private Key.

### 3. Solution 
Để giải quyết bài này, chúng ta cần một công cụ có khả năng đọc cấu trúc ASN.1 bên trong file PEM và tách biệt các thành phần của RSA (n, e, d, p, q). Thư viện **PyCryptodome** của Python là công cụ mạnh mẽ nhất cho việc này.

#### Các bước thực hiện:
1. **Cài đặt thư viện:** Sử dụng lệnh `pip install pycryptodome` (hoặc `py -m pip install pycryptodome` trên Windows).
2. **Đọc file PEM:** Tải file về và dùng hàm `open()` để đọc nội dung văn bản.
3. **Import khóa:** Sử dụng hàm `RSA.importKey()` để thư viện tự động giải mã cấu trúc phức tạp bên trong.
4. **Truy xuất thuộc tính `d`:** Đối tượng khóa sau khi import sẽ có sẵn thuộc tính `.d`.

### 3. Mã khai thác (Exploit Script)

```python
from Crypto.PublicKey import RSA
pem_content = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAzvKDt+EO+A6oE1LItSunkWJ8vN6Tgcu8Ck077joGDfG2NtxD
4vyQxGTQngr6jEKJuVz2MIwDcdXtFLIF+ISX9HfALQ3yiedNS80n/TR1BNcJSlzI
uqLmFxddmjmfUvHFuFLvxgXRga3mg3r7olTW+1fxOS0ZVeDJqFCaORRvoAYOgLgu
d2/E0aaaJi9cN7CjmdJ7Q3m6ryGuCwqEvZ1KgVWWa7fKcFopnl/fcsSecwbDV5hW
fmvxiAUJy1mNSPwkf5YhGQ+83g9N588RpLLMXmgt6KimtiWnJsqtDPRlY4Bjxdpu
V3QyUdo2ymqnquZnE/vlU/hn6/s8+ctdTqfSCwIDAQABAoIBAHw7HVNPKZtDwSYI
djA8CpW+F7+Rpd8vHKzafHWgI25PgeEhDSfAEm+zTYDyekGk1+SMp8Ww54h4sZ/Q
1sC/aDD7ikQBsW2TitVMTQs1aGIFbLBVTrKrg5CtGCWzHa+/L8BdGU84wvIkINMh
CtoCMCQmQMrgBeuFy8jcyhgl6nSW2bFwxcv+NU/hmmMQK4LzjV18JRc1IIuDpUJA
kn+JmEjBal/nDOlQ2v97+fS3G1mBAaUgSM0wwWy5lDMLEFktLJXU0OV59Sh/90qI
Jo0DiWmMj3ua6BPzkkaJPQJmHPCNnLzsn3Is920OlvHhdzfins6GdnZ8tuHfDb0t
cx7YSLECgYEA7ftHFeupO8TCy+cSyAgQJ8yGqNKNLHjJcg5t5vaAMeDjT/pe7w/R
0IWuScCoADiL9+6YqUp34RgeYDkks7O7nc6XuABi8oMMjxGYPfrdVfH5zlNimS4U
wl93bvfazutxnhz58vYvS6bQA95NQn7rWk2YFWRPzhJVkxvfK6N/x6cCgYEA3p21
w10lYvHNNiI0KBjHvroDMyB+39vD8mSObRQQuJFJdKWuMq+o5OrkC0KtpYZ+Gw4z
L9DQosip3hrb7b2B+bq0yP7Izj5mAVXizQTGkluT/YivvgXcxVKoNuNTqTEgmyOh
Pn6w+PqRnESsSFzjfWrahTCrVomcZmnUTFh0rv0CgYBETN68+tKqNbFWhe4M/Mtu
MLPhFfSwc8YU9vEx3UMzjYCPvqKqZ9bmyscXobRVw+Tf9llYFOhM8Pge06el74qE
IvvGMk4zncrn8LvJ5grKFNWGEsZ0ghYxJucHMRlaU5ZbM6PEyEUQqEKBKbbww65W
T3i7gvuof/iRbOljA9yzdwKBgQDT9Pc+Fu7k4XNRCon8b3OnnjYztMn4XKeZn7KY
GtW81eBJpwJQEj5OD3OnYQoyovZozkFgUoKDq2lJJuul1ZzuaJ1/Dk+lR3YZ6Wtz
ZwumCHnEmSMzWyOT4Rp2gEWEv1jbPbZl6XyY4wJG9n/OulqDbHy4+dj5ITb/r93J
/yLCBQKBgHa8XYMLzH63Ieh69VZF/7jO3d3lZ4LlMEYT0BF7synfe9q6x7s0ia9b
f6/QCkmOxPC868qhOMgSS48L+TMKmQNQSm9b9oy2ILlLA0KDsX5O/Foyiz1scwr7
nh6tZ+tVQCRvFviIEGkaXdEiBN4eTbcjfc5md/u9eA5N21Pzgd/G
-----END RSA PRIVATE KEY-----"""

key = RSA.importKey(pem_content)
print(key.d)
```

### 4. Kết quả
Sau khi chạy script, chương trình xuất ra một số nguyên cực lớn bắt đầu bằng `156827...`. Đây chính là giá trị cần tìm.
![alt text](assets/general/16_4.png)
* **Flag:** `15682700288056331364787171045819973654991149949197959929860861228180021707316851924456205543665565810892674190059831330231436970914474774562714945620519144389785158908994181951348846017432506464163564960993784254153395406799101314760033445065193429592512349952020982932218524462341002102063435489318813316464511621736943938440710470694912336237680219746204595128959161800595216366237538296447335375818871952520026993102148328897083547184286493241191505953601668858941129790966909236941127851370202421135897091086763569884760099112291072056970636380417349019579768748054760104838790424708988260443926906673795975104689`

![alt text](assets/general/16_5.png)



## **17. CERTainly not**
![alt text](assets/general/17_1.png)
### 1. Given
Một file chứng chỉ số RSA định dạng **DER** (`2048b-rsa-example-cert.der`)[cite: 2].
Định dạng DER là một phương pháp mã hóa nhị phân cho các cấu trúc dữ liệu ASN.1, thường được sử dụng trong các tiện ích của Windows hoặc các hệ thống nhúng[cite: 4].
Khác với định dạng PEM (thường thấy dưới dạng Base64 và có tiêu đề `-----BEGIN CERTIFICATE-----`), file DER chứa dữ liệu nhị phân thô không thể đọc trực tiếp bằng mắt thường[cite: 4].

### 2. Goal
Trích xuất giá trị **Modulus ($n$)** từ chứng chỉ X.509 này và đưa ra câu trả lời dưới dạng số nguyên thập phân[cite: 4].

### 3. Solution

#### **Phân tích kỹ thuật**
[cite_start]Chứng chỉ X.509 chứa nhiều thông tin như nhà phát hành (Issuer), thời hạn (Validity) và quan trọng nhất là **Public Key** của thực thể được cấp chứng chỉ[cite: 3, 4]. Vì đây là chứng chỉ RSA, Public Key sẽ bao gồm Modulus ($n$) và Public Exponent ($e$).

#### Các bước thực hiện
**Đọc file nhị phân:** Sử dụng Python mở file `.der` ở chế độ `rb` (read binary) để lấy toàn bộ dữ liệu thô[cite: 4].
**Import chứng chỉ:** Sử dụng thư viện mật mã (như `PyCryptodome`) thông qua hàm `RSA.importKey()`. [cite_start]Thư viện này đủ thông minh để tự động phân tích cấu trúc ASN.1 phức tạp bên trong chứng chỉ để tách lấy thành phần khóa công khai[cite: 4].
**Lấy giá trị $n$:** Truy xuất thuộc tính `.n` của đối tượng khóa đã import để lấy Modulus[cite: 4].

#### Mã khai thác (Python)
```python
from Crypto.PublicKey import RSA

# Đọc dữ liệu nhị phân từ file DER
with open("2048b-rsa-example-cert.der", "rb") as f:
    der_data = f.read()

# Phân tích chứng chỉ để trích xuất Public Key
key = RSA.importKey(der_data)

# Xuất Modulus ở dạng thập phân
print(key.n)
```
[cite_start][cite: 4]

---
### Kết quả:
`22825373692019530804306212864609512775374171823993708516509897631547513634635856375624003737068034549047677999310941837454378829351398302382629658264078775456838626207507725494030600516872852306191255492926495965536379271875310457319107936020730050476235278671528265817571433919561175665096171189758406136453987966255236963782666066962654678464950075923060327358691356632908606498231755963567382339010985222623205586923466405809217426670333410014429905146941652293366212903733630083016398810887356019977409467374742266276267137547021576874204809506045914964491063393800499167416471949021995447722415959979785959569497`


![alt text](assets/general/17_2.png)


## **18. SSH Keys**
![alt text](assets/general/18_1.png)
![alt text](assets/general/18_2.png)
### **1. Phân tích (Given)**
* **Dữ liệu:** Một file `bruce_rsa.pub` chứa khóa công khai SSH.
* **Định dạng:** Khóa SSH công khai có cấu trúc khác với file PEM truyền thống. Nó bắt đầu bằng loại thuật toán (`ssh-rsa`), theo sau là một chuỗi Base64 và cuối cùng là comment (email/tên máy).
* **Cấu trúc bên trong:** Chuỗi Base46 đó thực chất là các giá trị được mã hóa theo định dạng nhị phân của SSH, bao gồm:
    * Độ dài chuỗi "ssh-rsa" + chuỗi "ssh-rsa"
    * Độ dài số mũ $e$ + giá trị $e$
    * Độ dài Modulus $N$ + giá trị $N$

### 2. Goal
* Trích xuất giá trị Modulus $N$ từ file khóa này và chuyển nó sang dạng số nguyên thập phân (decimal integer).

### 3. Solution

1. Đọc nội dung file `.pub`.
2. Sử dụng `RSA.importKey()` để parse dữ liệu.
3. Truy cập thuộc tính `.n` của đối tượng khóa để lấy Modulus.

```python
import os
from Crypto.PublicKey import RSA

# Lấy đường dẫn thư mục của chính file script này
dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = "bruce_rsa_6e7ecd53b443a97013397b1a1ea30e14.pub"
full_path = os.path.join(dir_path, file_name)

with open(full_path, "r") as f:
    key = RSA.importKey(f.read())

print("Flag của bạn đây:")
print(key.n)
```

### 4. Kết quả
`3931406272922523448436194599820093016241472658151801552845094518579507815990600459669259603645261532927611152984942840889898756532060894857045175300145765800633499005451738872081381267004069865557395638550041114206143085403607234109293286336393552756893984605214352988705258638979454736514997314223669075900783806715398880310695945945147755132919037973889075191785977797861557228678159538882153544717797100401096435062359474129755625453831882490603560134477043235433202708948615234536984715872113343812760102812323180391544496030163653046931414723851374554873036582282389904838597668286543337426581680817796038711228401443244655162199302352017964997866677317161014083116730535875521286631858102768961098851209400973899393964931605067856005410998631842673030901078008408649613538143799959803685041566964514489809211962984534322348394428010908984318940411698961150731204316670646676976361958828528229837610795843145048243492909`

## **19. Transparency**

![alt text](assets/general/19_1.png)
![alt text](assets/general/19_2.png)
### Given
- Bối cảnh lý thuyết: Bài viết giải thích về cách hoạt động của chứng chỉ TLS/SSL khi kết nối HTTPS và vai trò của các tổ chức cấp phát chứng chỉ (Certificate Authority - CA). Nó cũng nêu ra rủi ro khi các CA bị hack (như vụ Comodo 2011 hay Symantec 2016), dẫn đến việc kẻ xấu có thể tạo ra chứng chỉ giả mạo cho bất kỳ trang web nào.

- Cơ chế Certificate Transparency (CT): Để khắc phục rủi ro trên, từ 2018, cơ chế "Minh bạch chứng chỉ" ra đời. Cơ chế này bắt buộc các CA phải ghi log (nhật ký) công khai mọi chứng chỉ mà họ cấp phát. Bất kỳ ai cũng có thể tra cứu các log này.

- File đính kèm: Đề bài cung cấp một file chứa RSA Public Key có định dạng PEM
```pem
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuYj06m5q4M8SsEQwKX+5
NPs2lyB2k7geZw4rP68eUZmqODeqxDjv5mlLY2nz/RJsPdks4J+y5t96KAyo3S5g
mDqEOMG7JgoJ9KU+4HPQFzP9C8Gy+hisChdo9eF6UeWGTioazFDIdRUK+gZm81c1
iPEhOBIYu3Cau32LRtv+L9vzqre0Ollf7oeHqcbcMBIKL6MpsJMG+neJPnICI36B
ZZEMu6v6f8zIKuB7VUHAbDdQ6tsBzLpXz7XPBUeKPa1Fk8d22EI99peHwWt0RuJP
0QsJnsa4oj6C6lE+c5+vVHa6jVsZkpl2PuXZ05a69xORZ4oq+nwzK8O/St1hbNBX
sQIDAQAB
-----END PUBLIC KEY-----
```
### Goal
- Dựa vào các tham số của khóa công khai (Public Key) trong file transparency.pem, bạn phải tìm ra tên miền phụ (subdomain) của trang web cryptohack.org đang sử dụng chứng chỉ TLS chứa khóa này.

- Truy cập vào subdomain đó để lấy được flag.

### Solution
- Lấy mã băm: Chạy lệnh lấy SHA-256 của public key.

```bash
openssl pkey -outform der -pubin -in transparency.pem | sha256sum
```
- Tra cứu: Vào crt.sh và tìm kiếm mã băm có được ở trên (29ab37df0a4e4d252f0cf12ad854bede59038fdd9cd652cbc5c222edd26d77d2).

- Tìm Subdomain: Nhìn vào kết quả, bạn sẽ thấy tên miền phụ: `thetransparencyflagishere.cryptohack.org`

- Nhận Flag: Truy cập đường dẫn https://thetransparencyflagishere.cryptohack.org/ để lấy cờ.

### Kết quả
![alt text](assets/general/20.png)
`crypto{c3rt1f1c4t3_tr4n5p4r3nc3_15_1mp0rt4nt}`