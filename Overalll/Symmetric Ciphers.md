# **Symmetric Ciphers**
## **1. Keyed Permutations**
### Given
Đề bài giới thiệu rằng AES là một **keyed permutation**.  
Nghĩa là với một khóa cố định, mỗi input block sẽ được ánh xạ tới đúng một output block duy nhất.

Đề cũng nói thêm:
- AES xử lý block 128 bit
- Có thể đảo ngược quá trình bằng cùng key
- Muốn giải mã đúng thì phải có sự tương ứng **một-một** giữa input và output

Câu hỏi cuối bài là:

**What is the mathematical term for a one-to-one correspondence?**

### Goal
Tìm thuật ngữ toán học của **one-to-one correspondence** và điền vào flag theo mẫu:

`crypto{term}`


### Solution

#### 1. Ý chính của đề

- Đề không yêu cầu code hay tính toán gì cả.  
Chỉ cần hiểu khái niệm toán học đứng sau câu “one-to-one correspondence”.

- Trong mật mã, nếu một thuật toán mã hóa có thể giải ngược lại chính xác, thì mỗi đầu vào phải tương ứng với đúng một đầu ra và ngược lại. Điều này đảm bảo không bị trùng lặp khi ánh xạ dữ liệu.

#### 2. Thuật ngữ toán học liên quan
Có 3 khái niệm dễ gây nhầm:

- **Injective**: hai phần tử đầu vào khác nhau thì không cho cùng một đầu ra
- **Surjective**: mọi phần tử ở tập đầu ra đều được ánh xạ tới
- **Bijective**: vừa injective vừa surjective

Cụm **one-to-one correspondence** trong toán học chính là **bijection**.

#### 3. Suy ra flag
Từ đó, từ khóa cần điền là: `bijection`

Nên flag là: `crypto{bijection}`


## **2. Resisting Brute Force**
### Given
Đề bài nói rằng nếu một block cipher đủ an toàn, thì đầu ra của AES phải không thể bị phân biệt với một hoán vị ngẫu nhiên của các bit.

Ngoài ra:
- Không nên có cách nào phá AES tốt hơn brute force quá nhiều
- Nếu có một tấn công nhanh hơn brute force, thì về mặt lý thuyết AES bị xem là “broken”
- Với AES-128, brute force gần như không khả thi vì không gian khóa quá lớn
- Tuy nhiên, thực tế có một tấn công trên AES tốt hơn brute force một chút
- Tấn công này giảm mức an toàn của AES-128 từ 128 bit xuống khoảng 126 bit

Câu hỏi cuối bài là:

**What is the name for the best single-key attack against AES?**

### Goal
Tìm tên của **tấn công single-key tốt nhất hiện nay đối với AES** và điền vào flag theo mẫu:

`crypto{term}`

### Solution

#### 1. Ý chính của đề
Bài này không yêu cầu lập trình hay tính toán.  
Chỉ cần đọc nội dung mô tả và nhận ra tên của cuộc tấn công được nhắc đến.

Đề cho biết:
- Tấn công này tốt hơn brute force
- Nhưng chỉ tốt hơn một chút
- Nó làm giảm độ an toàn từ 128 bit xuống còn khoảng 126.1 bit
- Đây là tấn công tốt nhất theo kiểu **single-key attack** trên AES

#### 2. Xác định tên tấn công
Tấn công nổi tiếng phù hợp đúng với mô tả này là: **biclique attack**

Đây là kết quả mật mã học thường được nhắc đến khi nói về AES:
- tốt hơn brute force một chút
- nhưng chưa đủ để đe dọa thực tế tới AES

#### 3. Suy ra flag
Vậy từ khóa cần điền là: `biclique`

Suy ra flag là: `crypto{biclique}`


## **3. Structure of AES**

### Given
Đề bài giới thiệu cấu trúc tổng quát của AES-128.  
AES bắt đầu với **key expansion / key schedule**, sau đó thực hiện **10 round** trên một **state**. State ban đầu chính là khối plaintext cần mã hóa, được biểu diễn dưới dạng **ma trận 4x4 byte**.

Các pha chính của AES được nêu trong đề:

1. **KeyExpansion / Key Schedule**  
   Từ khóa 128 bit, sinh ra 11 round key 128 bit để dùng trong các bước `AddRoundKey`.

2. **Initial key addition**  
   Thực hiện `AddRoundKey`, tức là XOR round key đầu tiên với state.

3. **Round**  
   Lặp 10 lần, gồm 9 round chính và 1 final round, với các bước:
   - `SubBytes`: thay mỗi byte bằng một byte khác theo bảng S-box
   - `ShiftRows`: dịch các hàng trong state
   - `MixColumns`: trộn các cột bằng phép nhân ma trận
   - `AddRoundKey`: XOR state với round key hiện tại

Đề cho sẵn file `matrix.py`, trong đó có hàm `bytes2matrix(text)` để chuyển 16 byte thành ma trận 4x4, và yêu cầu viết hàm `matrix2bytes(matrix)` để chuyển ma trận đó ngược lại thành bytes. :contentReference[oaicite:0]{index=0}

Nội dung file:

```python
def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    ????

matrix = [
    [99, 114, 121, 112],
    [116, 111, 123, 105],
    [110, 109, 97, 116],
    [114, 105, 120, 125],
]

print(matrix2bytes(matrix))
```
### Goal
Hiểu cách biểu diễn state của AES dưới dạng ma trận 4x4 và viết hàm `matrix2bytes(matrix)` để chuyển ma trận đó về lại dãy bytes ban đầu, từ đó lấy plaintext làm flag.

### Solution

#### 1. Ý tưởng của bài
Đề cho sẵn hàm `bytes2matrix(text)` để đổi một block 16 byte thành ma trận 4x4.  
Vì vậy yêu cầu của bài là làm chiều ngược lại: từ ma trận 4x4, ghép các phần tử lại theo đúng thứ tự để thu được dãy bytes ban đầu.

Hàm đã cho:

```python
def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]
```
Code tìm FLAG
```python
def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    return bytes([x for row in matrix for x in row])

matrix = [
    [99, 114, 121, 112],
    [116, 111, 123, 105],
    [110, 109, 97, 116],
    [114, 105, 120, 125],
]

print(matrix2bytes(matrix))
```

<img width="1128" height="179" alt="image" src="https://github.com/user-attachments/assets/9a43c9aa-3389-491f-a8da-73af94b6a2bb" />


## **4.Round Keys**

### Given
Đề bài giới thiệu về giai đoạn **KeyExpansion** của AES.  
Từ khóa ban đầu dài 16 byte, AES sinh ra **11 ma trận khóa 4x4** gọi là **round key**. Các round key này được dùng ở những bước `AddRoundKey` trong quá trình mã hóa.

Đề cũng nói rằng:
- bước **initial key addition** chỉ có một lần `AddRoundKey`
- `AddRoundKey` thực hiện bằng cách **XOR state hiện tại với round key hiện tại**
- đây là bước duy nhất mà khóa được trộn trực tiếp vào state
- `AddRoundKey` cũng xuất hiện ở cuối mỗi round

Cuối bài, đề yêu cầu:

- hoàn thiện hàm `add_round_key`
- sau đó dùng hàm `matrix2bytes` để lấy ra flag

### Goal
Hiểu vai trò của bước `AddRoundKey` trong AES và hoàn thiện hàm `add_round_key(state, round_key)` bằng cách XOR từng phần tử của `state` với phần tử tương ứng của `round_key`, sau đó dùng `matrix2bytes` để đổi kết quả về plaintext và lấy flag.

### Solution

#### Ý tưởng của bài
Trong AES, `AddRoundKey` là bước trộn khóa vào state.  
Cách làm rất đơn giản:

- `state` là ma trận 4x4
- `round_key` cũng là ma trận 4x4
- mỗi phần tử ở cùng vị trí sẽ được XOR với nhau

Tức là:

```python
new_state[i][j] = state[i][j] ^ round_key[i][j]
````
Code tìm FLAG

```python
def matrix2bytes(matrix):
    return bytes([x for row in matrix for x in row])

def add_round_key(s, k):
    return [[s[i][j] ^ k[i][j] for j in range(4)] for i in range(4)]

state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]

result = add_round_key(state, round_key)
flag = matrix2bytes(result)

print(flag)
print(flag.decode())
```
<img width="1095" height="147" alt="image" src="https://github.com/user-attachments/assets/aaed33a9-36db-45c9-a9e3-4361af5ca819" />



## **5. Confusion through Substitution**

### Given
Đề bài giới thiệu bước **SubBytes** trong mỗi round của AES.

- Ở bước này, mỗi byte của **state matrix** sẽ được thay thế bằng một byte khác thông qua một bảng tra cứu `16 x 16`
- Bảng tra cứu đó được gọi là **Substitution box** hay **S-box**
- Mục đích của S-box là tạo ra **confusion** theo ý tưởng của Claude Shannon, tức là làm cho mối quan hệ giữa **ciphertext** và **key** trở nên phức tạp nhất có thể
- Nếu một cipher có độ confusion kém, mối quan hệ giữa plaintext, ciphertext và key có thể bị biểu diễn gần đúng bằng các hàm tuyến tính hoặc đa thức bậc thấp, từ đó dễ bị phân tích
- AES sử dụng một S-box có độ **phi tuyến cao**, được xây dựng từ:
  - nghịch đảo modulo trong trường Galois `2^8`
  - sau đó áp dụng một phép biến đổi affine

Đề bài nói thêm rằng để tạo S-box, giá trị của hàm này đã được tính sẵn cho toàn bộ input từ `0x00` đến `0xff` rồi lưu vào bảng tra cứu.

Cuối bài, đề yêu cầu:

- cài đặt hàm `sub_bytes`
- đưa state matrix đi qua **inverse S-box**
- sau đó đổi kết quả về bytes để lấy flag


### Goal
Viết hàm `sub_bytes(state, sbox)` để thay thế từng byte trong state bằng giá trị tương ứng trong **inverse S-box**, rồi dùng `matrix2bytes` chuyển ma trận kết quả về bytes để đọc ra flag.

### Solution

#### 1. Ý tưởng của bài
Trong AES, bước `SubBytes` hoạt động bằng cách:

- lấy từng byte trong state
- dùng byte đó làm chỉ số tra cứu trong S-box
- thay byte cũ bằng byte mới

Ở bài này, đề yêu cầu dùng **inverse S-box**, tức là ta sẽ không tra trong S-box thuận mà tra trong bảng nghịch đảo.

Vì state là ma trận `4 x 4`, nên ta chỉ cần:
- duyệt toàn bộ 16 phần tử
- với mỗi phần tử `x`, thay bằng `inv_s_box[x]`

Công thức:

```python
new_state[i][j] = inv_s_box[state[i][j]]
```
#### Cách biết hàm sub_byte
```python
def sub_bytes(s, sbox):
    return [[sbox[s[i][j]] for j in range(4)] for i in range(4)]
```
#### Đổi ma trận về kết quả bytes
```python
result = sub_bytes(state, inv_s_box)
print(matrix2bytes(result))
```
#### Code tìm FLAG
```python
inv_s_box = (
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d,
)

def matrix2bytes(matrix):
    return bytes([x for row in matrix for x in row])

def sub_bytes(s, sbox):
    return [[sbox[s[i][j]] for j in range(4)] for i in range(4)]

state = [
    [251, 64, 183, 114],
    [95, 164, 104, 13],
    [120, 211, 49, 104],
    [56, 90, 132, 237],
]

result = sub_bytes(state, inv_s_box)
flag = matrix2bytes(result)

print(flag)
print(flag.decode())
```
#### FLAG: `crypto{l1n34rly}`


## **6. Diffusion through Permutation**

### Given
Đề bài giải thích về tính chất **diffusion** trong AES.

- Nếu **confusion** làm cho mối quan hệ giữa ciphertext và key trở nên phức tạp, thì **diffusion** làm cho ảnh hưởng của mỗi phần của input lan ra toàn bộ output
- Một thay đổi nhỏ ở plaintext nên dẫn đến thay đổi ở rất nhiều bit của ciphertext; hiệu ứng này được gọi là **avalanche effect**
- Trong AES, hai bước chính tạo diffusion là:
  - `ShiftRows`
  - `MixColumns`

Đề mô tả cụ thể:

#### 1. ShiftRows
`ShiftRows` là phép hoán vị đơn giản trên các hàng của state matrix:

- hàng 0: giữ nguyên
- hàng 1: dịch trái 1 ô
- hàng 2: dịch trái 2 ô
- hàng 3: dịch trái 3 ô

Ở bài này, đề cho sẵn **forward ShiftRows**, nhưng yêu cầu ta viết hàm **`inv_shift_rows`** để đảo ngược phép biến đổi đó.

#### 2. MixColumns
`MixColumns` thực hiện phép nhân ma trận trong trường Galois của Rijndael trên các cột của state matrix.  
Mỗi byte trong một cột sẽ ảnh hưởng đến toàn bộ các byte còn lại trong cùng cột, từ đó tạo ra diffusion mạnh hơn.

Đề cho sẵn code của:
- `mix_columns`
- `inv_mix_columns`
- forward `shift_rows`

Cuối bài, đề yêu cầu:

- cài đặt `inv_shift_rows`
- lấy `state`
- chạy `inv_mix_columns(state)`
- sau đó `inv_shift_rows(state)`
- cuối cùng đổi về bytes để lấy flag

### Goal
Viết hàm `inv_shift_rows(state)` để đảo ngược phép dịch hàng của AES, sau đó áp dụng `inv_mix_columns` rồi `inv_shift_rows` lên state, cuối cùng dùng `matrix2bytes` để chuyển kết quả về bytes và đọc ra flag.

### Solution

#### 1. Ý tưởng của bài
Trong AES:

- `ShiftRows` dịch trái các hàng
- nên `inv_shift_rows` sẽ làm điều ngược lại: **dịch phải**

Cụ thể:
- hàng 0: giữ nguyên
- hàng 1: dịch phải 1 ô
- hàng 2: dịch phải 2 ô
- hàng 3: dịch phải 3 ô

Nếu viết theo kiểu Python với slicing thì rất gọn.

#### 2. Cách viết `inv_shift_rows`
Ta có thể viết:

```python
def inv_shift_rows(s):
    s[1] = s[1][-1:] + s[1][:-1]
    s[2] = s[2][-2:] + s[2][:-2]
    s[3] = s[3][-3:] + s[3][:-3]
    return s
```
Code tìm FLag
```python
def matrix2bytes(matrix):
    return bytes([x for row in matrix for x in row])

def inv_shift_rows(s):
    s[1] = s[1][-1:] + s[1][:-1]
    s[2] = s[2][-2:] + s[2][:-2]
    s[3] = s[3][-3:] + s[3][:-3]
    return s

state = inv_mix_columns(state)
state = inv_shift_rows(state)

flag = matrix2bytes(state)
print(flag)
print(flag.decode())
```
#### FLAG `crypto{d1ffUs3R}`


## **7. Bringing It All Together**

### Given
Đề bài nói rằng từ các challenge trước, ta đã xây dựng gần đủ các thành phần của AES, gồm:

- `SubBytes` / `InvSubBytes`
- `ShiftRows` / `InvShiftRows`
- `MixColumns` / `InvMixColumns`
- `AddRoundKey`
- `KeyExpansion`

Ở bài này, đề cho sẵn:

- hàm `expand_key(master_key)` để sinh các **round key** từ khóa ban đầu 
- giá trị:

```python
key        = b'\xc3,\\\xa6\xb5\x80^\x0c\xdb\x8d\xa5z*\xb6\xfe\\'
ciphertext = b'\xd1O\x14j\xa4+O\xb6\xa1\xc4\x08B)\x8f\x12\xdd'
```
Khung hàm được cho
```python
def decrypt(key, ciphertext):
    round_keys = expand_key(key) 
    for i in range(N_ROUNDS - 1, 0, -1):
        pass 
    return plaintext
```
### GOAL
Hoàn thiện hàm decrypt(key, ciphertext) để giải mã ciphertext AES-128 bằng các thành phần đã viết ở các bài trước, rồi lấy plaintext làm flag.

### Solution

#### 1. Ý tưởng của bài

Giải mã AES là đi **ngược** quá trình mã hóa.

Nếu mã hóa có dạng:

1. `AddRoundKey`
2. lặp các round với:
   - `SubBytes`
   - `ShiftRows`
   - `MixColumns`
   - `AddRoundKey`
3. round cuối bỏ `MixColumns`

thì giải mã sẽ đi ngược lại:

1. đổi ciphertext thành state matrix
2. `AddRoundKey` với **round key cuối**
3. với các round từ cuối về đầu:
   - `InvShiftRows`
   - `InvSubBytes`
   - `AddRoundKey`
   - `InvMixColumns`
4. round cuối cùng:
   - `InvShiftRows`
   - `InvSubBytes`
   - `AddRoundKey` với round key đầu
5. đổi state matrix về bytes

#### Code tìm FLAG:
```py
N_ROUNDS = 10

s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

key        = b'\xc3,\\\xa6\xb5\x80^\x0c\xdb\x8d\xa5z*\xb6\xfe\\'
ciphertext = b'\xd1O\x14j\xa4+O\xb6\xa1\xc4\x08B)\x8f\x12\xdd'


def bytes2matrix(text):
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]


def matrix2bytes(matrix):
    return bytes(sum(matrix, []))


def add_round_key(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]


def sub_bytes(s, sbox):
    for i in range(4):
        for j in range(4):
            s[i][j] = sbox[s[i][j]]


def inv_sub_bytes(s):
    sub_bytes(s, inv_s_box)


def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


def inv_shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]


def xtime(a):
    return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def mix_single_column(a):
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)


def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])


def inv_mix_columns(s):
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v

    mix_columns(s)


def expand_key(master_key):
    r_con = (
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    )

    key_columns = bytes2matrix(master_key)
    iteration_size = len(master_key) // 4

    i = 1
    while len(key_columns) < (N_ROUNDS + 1) * 4:
        word = list(key_columns[-1])

        if len(key_columns) % iteration_size == 0:
            word.append(word.pop(0))
            word = [s_box[b] for b in word]
            word[0] ^= r_con[i]
            i += 1
        elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
            word = [s_box[b] for b in word]

        word = bytes(a ^ b for a, b in zip(word, key_columns[-iteration_size]))
        key_columns.append(word)

    return [key_columns[4 * i: 4 * (i + 1)] for i in range(len(key_columns) // 4)]


def decrypt(key, ciphertext):
    round_keys = expand_key(key)

    state = bytes2matrix(ciphertext)

    add_round_key(state, round_keys[-1])

    for i in range(N_ROUNDS - 1, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, round_keys[i])
        inv_mix_columns(state)

    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, round_keys[0])

    return matrix2bytes(state)


flag = decrypt(key, ciphertext)
print(flag)
print(flag.decode())
```

#### FLAG: `crypto{MYAES128}`
<img width="1277" height="161" alt="image" src="https://github.com/user-attachments/assets/7ea5be5e-6808-4b18-acf3-3127241ff3da" />


## **8. Modes of Operation Starter**
### Given
- CryptoHack cung cấp cho chúng ta một giao diện API tại đường dẫn: https://aes.cryptohack.org/block_cipher_starter/.
  
- Hệ thống cung cấp mã nguồn tham khảo với hai  chính:

<div align="center">

| Hàm | Chức năng | Trả về |
| :--- | :--- | :--- |
| `encrypt_flag()` | Mã hóa Flag bí mật bằng AES. | Một chuỗi Hex chứa bản mã (`ciphertext`). |
| `decrypt(ciphertext)` | Giải mã một chuỗi Hex bản mã bất kỳ. | Một chuỗi Hex chứa bản rõ (`plaintext`). |

</div>

### Goal
- Vì Flag đã được mã hóa, ta cần sử dụng chức năng `decrypt` của hệ thống để giải mã bản mã mà chức năng `encrypt_flag` trả về.

### Solution
- Nhấn vào nút `encrypt_flag()`, ta sẽ nhận được một chuỗi Hex:

    ![](assets/symmeric%20ciphers/8-1.png)

- Copy chuỗi đó và dán vào ô tham số của hàm decrypt(ciphertext), sau đó nhấn nút **Decrypt**. Kết quả trả về là một chuỗi Hex mới.

    ![](assets/symmeric%20ciphers/8-2.png)

- Sử dụng HEX ENCODER/DECODER để giải mã.

    ![](assets/symmeric%20ciphers/8-3.png)


## **9. Passwords as Keys**
### Given
- Source code server:
    ```python
    import hashlib, random
    from Crypto.Cipher import AES

    with open("/usr/share/dict/words") as f:
        words = [w.strip() for w in f.readlines()]

    # Key được tạo từ MD5 hash của một từ ngẫu nhiên trong từ điển
    keyword = random.choice(words)
    KEY = hashlib.md5(keyword.encode()).digest()  # <- KEY yếu!

    @chal.route('/passwords_as_keys/encrypt_flag/')
    def encrypt_flag():
        cipher = AES.new(KEY, AES.MODE_ECB)
        encrypted = cipher.encrypt(FLAG.encode())
        return {"ciphertext": encrypted.hex()}

    @chal.route('/passwords_as_keys/decrypt/<ciphertext>/<password_hash>/')
    def decrypt(ciphertext, password_hash):
        key = bytes.fromhex(password_hash)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(bytes.fromhex(ciphertext))
        return {"plaintext": decrypted.hex()}
    ```

- Key AES 128-bit được tạo bằng cách:
    - Chọn ngẫu nhiên một từ trong file `/usr/share/dict/words` (~235.000 từ)
    - Hash từ đó bằng **MD5** -> dùng làm key

    > **CSPRNG (Cryptographically Secure Pseudorandom Number Generator):** Bộ sinh số ngẫu nhiên đạt chuẩn mật mã — không thể đoán được output tiếp theo dù biết tất cả output trước. `random.choice()` trong Python **không** phải CSPRNG và key từ hash của từ điển có thể brute-force.

### Goal
- Brute-force lại key bằng cách thử MD5 hash của toàn bộ từ trong từ điển, giải mã ciphertext offline mà không cần gọi server.

### Solution
- **Ý tưởng:** Dictionary Attack

    Key space thực tế chỉ là ~235.000 từ — cực kỳ nhỏ so với $2^{128}$ khả năng của AES-128. Với mỗi từ, ta tính `MD5(word)` rồi thử giải mã ciphertext, kiểm tra xem kết quả có bắt đầu bằng `crypto{` không.

    > **Dictionary Attack:** Thay vì brute-force toàn bộ key space, ta chỉ thử các key được sinh ra từ một tập từ điển có sẵn. Hiệu quả khi người dùng dùng từ thông thường làm password.

    > **Tại sao MD5 không an toàn để tạo key?** MD5 là hàm hash nhanh — máy tính hiện đại có thể tính hàng tỷ MD5/giây. Việc hash một từ điển nhỏ tốn chưa đến 1 giây. Key cần được tạo từ **nguồn entropy thực sự ngẫu nhiên** (`os.urandom()`), không phải từ password.

- **Bước 1 — Tải từ điển và lấy ciphertext:**
    ```python
    # Tải từ điển (giống file trên server)
    wget https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words -O words.txt
    ```

    ```python
    import requests

    # Lấy ciphertext từ server
    r = requests.get("https://aes.cryptohack.org/passwords_as_keys/encrypt_flag/")
    ciphertext_hex = r.json()["ciphertext"]
    ```

- **Bước 2 — Brute-force offline:**
    ```python
    import hashlib
    from Crypto.Cipher import AES

    # Đọc toàn bộ từ điển
    with open("words.txt") as f:
        words = [w.strip() for w in f.readlines()]

    # Thử từng từ làm password
    for word in words:
        # Tạo key bằng cách MD5 hash từ → giống hệt logic server
        key = hashlib.md5(word.encode()).digest()
        
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = cipher.decrypt(bytes.fromhex(ciphertext_hex))
        
        # Kiểm tra known plaintext: flag luôn bắt đầu bằng "crypto{"
        if plaintext.startswith(b"crypto{"):
            print(f"Password: {word}")
            print(f"Flag: {plaintext.decode()}")
            break
    ```
    
- **Kết quả:**

    ![](assets/symmeric%20ciphers/9.png)


## **10. ECB CBC WTF**
### Given
- Server cung cấp 2 **API endpoint**:
    ```python
    # Mã hóa flag bằng AES-CBC với IV (Initialization Vector - 16 byte đầu tiên) ngẫu nhiên
    # Trả về: iv (16 bytes) + ciphertext (hex)
    GET /ecbcbcwtf/encrypt_flag/

    # Nhận vào: ciphertext hex bất kỳ
    # Giải mã bằng AES-ECB
    GET /ecbcbcwtf/decrypt/<ciphertext>/
    ```

- **Source code server:**
    ```python
    @chal.route('/ecbcbcwtf/decrypt/<ciphertext>/')
    def decrypt(ciphertext):
        ciphertext = bytes.fromhex(ciphertext)
        cipher = AES.new(KEY, AES.MODE_ECB)   # Giải mã bằng ECB
        decrypted = cipher.decrypt(ciphertext)
        return {"plaintext": decrypted.hex()}

    @chal.route('/ecbcbcwtf/encrypt_flag/')
    def encrypt_flag():
        iv = os.urandom(16)
        cipher = AES.new(KEY, AES.MODE_CBC, iv)  # Mã hóa bằng CBC
        encrypted = cipher.encrypt(FLAG.encode())
        ciphertext = iv.hex() + encrypted.hex()  # Trả về IV + ciphertext
        return {"ciphertext": ciphertext}
    ```

### Goal
- Khai thác sự không khớp giữa **mã hóa CBC** và **giải mã ECB** để khôi phục flag gốc.

### Solution
- **Ý tưởng:** Mổ xẻ CBC bằng ECB oracle.

    Trước tiên, ta cần hiểu cách CBC decryption hoạt động:
    > **CBC Decryption:** Mỗi block plaintext được tính bằng: $P_i = \text{ECB\_Decrypt}(C_i) \oplus C_{i-1}$
    > 
    > Với block đầu tiên: $P_1 = \text{ECB\_Decrypt}(C_1) \oplus IV$

    Vì server cho phép gọi `ECB_Decrypt(C_i)` trực tiếp trên từng block ciphertext, ta có thể thực hiện bước XOR để khôi phục plaintext.

- **Bước 1 — Lấy ciphertext từ server:**
    ```python
    GET /ecbcbcwtf/encrypt_flag/
    -> {"ciphertext": "IV(32 hex) + C1(32 hex) + C2(32 hex)"}
    ```

    Tách ciphertext thành:
$$ciphertext\_hex = IV || C1 || C2$$

- **Bước 2 — Giải mã từng block bằng ECB oracle:**

    Gửi từng block `C1`, `C2` qua endpoint `/decrypt/`:
    ```python
    ECB_Decrypt(C1) -> D1  (đây là P1 ⊕ IV chưa XOR)
    ECB_Decrypt(C2) -> D2  (đây là P2 ⊕ C1 chưa XOR)
    ```

- **Bước 3 — XOR để khôi phục plaintext:**

    $P1 = D1 ⊕ IV$       (block đầu XOR với IV)

    $P2 = D2 ⊕ C1$       (block sau XOR với block cipher trước)

    $FLAG = P1 + P2$

    ```python
    import requests
    from pwn import xor

    BASE = "https://aes.cryptohack.org"

    def encrypt_flag():
        # Lấy IV + ciphertext CBC của flag từ server.
        r = requests.get(f"{BASE}/ecbcbcwtf/encrypt_flag/")
        return r.json()["ciphertext"]

    def ecb_decrypt(block_hex):
        # Giải mã một block bằng AES-ECB (raw, chưa XOR).
        r = requests.get(f"{BASE}/ecbcbcwtf/decrypt/{block_hex}/")
        return bytes.fromhex(r.json()["plaintext"])

    # Bước 1: Lấy ciphertext và tách thành IV, C1, C2
    ciphertext_hex = encrypt_flag()
    iv = bytes.fromhex(ciphertext_hex[:32])    # 16 bytes đầu là IV
    c1 = bytes.fromhex(ciphertext_hex[32:64]) # block ciphertext 1
    c2 = bytes.fromhex(ciphertext_hex[64:])   # block ciphertext 2

    # Bước 2: Giải mã từng block bằng ECB oracle
    d1 = ecb_decrypt(ciphertext_hex[32:64])   # ECB_Decrypt(C1)
    d2 = ecb_decrypt(ciphertext_hex[64:])     # ECB_Decrypt(C2)

    # Bước 3: XOR để ra plaintext (mô phỏng lại CBC decryption thủ công)
    p1 = xor(d1, iv)  # P1 = ECB_Decrypt(C1) ⊕ IV
    p2 = xor(d2, c1)  # P2 = ECB_Decrypt(C2) ⊕ C1

    # Flag
    print((p1 + p2).decode())
    ```

- **Flag:**

    ![](assets/symmeric%20ciphers/10.png)

- **Tại sao attack này hoạt động?**

    Bình thường, CBC decryption là một black-box — server dùng cùng một key cho cả hai bước `ECB decrypt` và `XOR`. Nhưng ở đây server đã expose bước ECB decrypt ra ngoài, cho phép ta tự XOR thủ công:

    ```text
    CBC Decrypt = ECB_Decrypt(Cᵢ)  ⊕  Cᵢ₋₁
                ↑ server làm giúp    ↑ ta tự XOR
    ```

## **11. ECB Oracle**
### Given
- Server cung cấp 1 endpoint duy nhất:
    ```python
    @chal.route('/ecb_oracle/encrypt/<plaintext>/')
    def encrypt(plaintext):
        plaintext = bytes.fromhex(plaintext)
        plaintext = plaintext + FLAG.encode()  # input ghép trước flag
        padded = pad(plaintext)
        cipher = AES.new(KEY, AES.MODE_ECB)
        ciphertext = cipher.encrypt(padded)
        return {"ciphertext": ciphertext.hex()}
    ```

- Có 3 điều quan trọng cần chú ý:

    - Ta kiểm soát **prefix**, flag nằm phía sau
    
    - Key là **cố định** — cùng plaintext block luôn cho cùng ciphertext block

    - Chỉ có encrypt, không có decrypt

    > **AES-ECB (Electronic Codebook)**: Mỗi block 16 byte plaintext được mã hóa độc lập bằng cùng một key. Không có XOR với block trước như CBC. Hệ quả: hai block plaintext giống nhau -> hai block ciphertext giống hệt nhau — đây là điểm yếu bị khai thác.

    > 💡 **Oracle** là một "hộp đen" mà ta gửi input vào và nhận output ra, nhưng không thấy bên trong (không biết key). Ở challenge này, oracle chính là `server endpoint` — ta không có key nhưng có thể nhờ server mã hóa bất kỳ plaintext nào. Chỉ cần hỏi oracle đủ nhiều lần với input được chọn khéo léo, ta có thể khôi phục thông tin bí mật mà không cần biết key.

### Goal
- Khôi phục toàn bộ flag từng ký tự một, không cần biết key, chỉ dùng oracle encrypt.

### Solution
- **Ý tưởng:** Byte-at-a-time ECB Decryption

    - Vì ta kiểm soát prefix và ECB mã hóa từng block độc lập, ta có thể đẩy từng byte chưa biết của flag vào đúng **vị trí cuối của một block**, sau đó brute-force 256 khả năng để tìm byte đó.

    - Nguyên lý hoạt động đơn giản: nếu block `[A A A A A A A A A A A A A A A ?]` cho ra ciphertext block `X`, thì ta chỉ cần thử tất cả `?` từ 0–255 cho đến khi encrypt của `[A×15 + ?]` cũng cho ra block `X`.

- **Bước 1 — Hiểu cách bố trí block:**

    `BLOCK_SIZE = 16 byte`. Mỗi block hex = 32 ký tự. Oracle mã hóa:

    ```
    ECB( input || FLAG )
    ```

    Với byte thứ `i` của flag (đánh số từ 1), ta tính số byte padding cần gửi để byte đó rơi vào cuối block:

    ```
    pad_length = (BLOCK_SIZE - (i % BLOCK_SIZE)) % BLOCK_SIZE
    ```

    Minh họa cụ thể:

    ```
    i=1:  pad="A"×15 → block0 = [A A A A A A A A A A A A A A A | F₁]
    i=2:  pad="A"×14 → block0 = [A A A A A A A A A A A A A A | F₁ F₂]
    i=3:  pad="A"×13 → block0 = [A A A A A A A A A A A A A | F₁ F₂ F₃]
    ...
    i=15: pad="A"×1  → block0 = [A | F₁ F₂ F₃ F₄ F₅ F₆ F₇ F₈ F₉ F₁₀ F₁₁ F₁₂ F₁₃ F₁₄ F₁₅]
    i=16: pad_length = (16 - 16%16) % 16 = 0 -> URL rỗng!
    ```

    Khi `pad_length == 0`, URL thành `.../encrypt//` -> server trả 404. Xử lý bằng cách thêm 1 block đệm `("A" × 16)` và dịch `target_block_index` sang phải 1:

    ```python
    if pad_length == 0:
        padding = "A" * BLOCK_SIZE    # thêm 1 block để URL hợp lệ
        target_block_index += 1       # byte cần tìm dịch sang block tiếp theo
    ```

    Sau khi fix, vòng lặp tiếp tục hoàn toàn tự nhiên sang block 1, block 2, ...

- **Bước 2 — Lấy block ciphertext tham chiếu:**

    Gửi `padding` (không có flag đã biết) lên oracle. Cắt đúng block chứa byte cần tìm:

    ```python
    target_ciphertext = encrypt(padding)
    start_idx  = target_block_index * 32   # mỗi block = 32 hex chars
    end_idx    = start_idx + 32
    target_block = target_ciphertext[start_idx:end_idx]
    ```

    Lúc này `target_block` là mã hóa của `[padding + flag_đã_biết + byte_cần_tìm]` — ta chưa biết byte cuối cùng.

- **Bước 3 — Brute-force byte tiếp theo:**

    Với mỗi ký tự `c` trong `string.printable` (95 ký tự in được), xây dựng chuỗi:

    ```
    guess = padding + known_flag + c
    ```

    Gửi lên oracle, cắt cùng block index, so sánh với `target_block`:

    ```
    Nếu encrypt(guess)[start:end] == target_block → c chính là byte tiếp theo của flag!
    ```

    Vì sao đúng? Vì:

    ```
    target_block  = ECB_encrypt( padding + F₁F₂...Fₙ + F(n+1) )
    guess_block   = ECB_encrypt( padding + F₁F₂...Fₙ + c      )
    → Khi c == F(n+1): hai block plaintext giống nhau -> ciphertext giống nhau
    ```

    **Tối ưu:** gửi song song 95 request cùng lúc thay vì tuần tự, cancel ngay khi tìm ra đáp án:

    ```python
    def _find_next_char(executor, padding, known_flag, start_idx, end_idx, target_block):
        # Gửi tất cả 95 request song song
        futures = {
            executor.submit(encrypt, padding + known_flag + char): char
            for char in alphabet
        }
        found_char = None
        try:
            for future in as_completed(futures):  # xử lý future nào về trước
                char = futures[future]
                guess_block = future.result()[start_idx:end_idx]
                if guess_block == target_block:
                    found_char = char
                    break  # tìm thấy -> thoát ngay
        finally:
            for future in futures:
                future.cancel()  # hủy các request chưa gửi
        return found_char
    ```

- **Bước 4 — Lặp cho đến khi tìm hết flag:**

    ```python
    flag = ""
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for i in range(1, MAX_FLAG_LEN + 1):
            # Tính padding và target block (như bước 1)
            ...
            # Brute-force ký tự tiếp theo (như bước 3)
            next_char = _find_next_char(...)
            flag += next_char
            print(f"Flag: {flag}")
            if flag.endswith("}"):  # flag kết thúc bằng "}"
                break
    ```

- **Kết quả:**

    ![](assets/symmeric%20ciphers/11.png)

## **12. Flipping Cookie**
### Given
- Server có 2 endpoint:

    ```python
    @chal.route('/flipping_cookie/get_cookie/')
    def get_cookie():
        expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
        cookie = f"admin=False;expiry={expires_at}".encode()
        iv = os.urandom(16)                          # IV ngẫu nhiên mỗi lần
        padded = pad(cookie, 16)
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(padded)
        ciphertext = iv.hex() + encrypted.hex()      # Trả về IV + ciphertext
        return {"cookie": ciphertext}

    @chal.route('/flipping_cookie/check_admin/<cookie>/<iv>/')
    def check_admin(cookie, iv):
        cookie = bytes.fromhex(cookie)
        iv = bytes.fromhex(iv)
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(cookie))
        if b"admin=True" in decrypted.split(b";"):   # Kiểm tra admin=True
            return {"flag": FLAG}
        return {"error": "Only admin can read the flag"}
    ```

- Có hai điểm quan trọng cần lưu ý:

    - Cookie plaintext luôn là `admin=False;expiry=...`

    - Endpoint `check_admin` nhận **cookie và IV riêng biệt**, do đó ta kiểm soát được IV.

### Goal
- Thay đổi cookie sao cho server giải mã ra chuỗi chứa `admin=True` thay vì `admin=False` để lấy flag mà không cần biết key.

### Solution
- **Ý tưởng:** CBC Bit-Flipping Attack

    Trước tiên, ta cần hiểu cách **CBC decryption** hoạt động:
    $$P_i = \text{AES\_Decrypt}(C_i) \oplus C_{i-1}$$

    Với block đầu tiên (i=0), không có block trước nên dùng IV:

    $$P_0 = \text{AES\_Decrypt}(C_0) \oplus IV$$

    > **CBC Bit-Flipping Attack:** Vì plaintext block 0 được XOR trực tiếp với IV trong quá trình decrypt, nếu ta thay đổi IV thì plaintext block 0 thay đổi theo, mà ciphertext block 0 vẫn giữ nguyên. Server cho phép ta gửi IV tùy ý, nên ta có thể kiểm soát hoàn toàn plaintext block 0 sau khi decrypt.

- **Bước 1 — Lấy cookie từ server:**

    ```
    GET /flipping_cookie/get_cookie/
    → {"cookie": "IV(32 hex chars) + C0(32 hex) + C1(32 hex)..."}
    ```

    Tách ra ta được:

    ```python
    iv = bytes.fromhex(cookie_hex[:32])   # 16 bytes đầu
    ct = cookie_hex[32:]                  # phần ciphertext
    ```

    Plaintext gốc của block 0 là:

    ```
    P0 = "admin=False;expi"   (16 byte đầu)
    ```

- **Bước 2 — Tính IV mới để flip bit:**

    Ta muốn sau khi decrypt, block 0 có dạng `"admin=True;\x00\x00\x00\x00\x00"` (hoặc bất kỳ thứ gì chứa `admin=True`).

    Từ công thức CBC decrypt:
    $$P_0 = \text{AES\_Decrypt}(C_0) \oplus IV$$

    Đặt `D0 = AES_Decrypt(C0)`, ta có `P0 = D0 ⊕ IV`. Suy ra:
    $$D_0 = P_0 \oplus IV$$

    Ta muốn plaintext mới `P'0` sau khi decrypt với `IV'` mới:
    $$P'_0 = D_0 \oplus IV' \implies IV' = D_0 \oplus P'_0$$

    Thay `D0 = P0 ⊕ IV` vào:
    $$IV' = (P_0 \oplus IV) \oplus P'_0 = IV \oplus P_0 \oplus P'_0$$
    
    **Công thức trên có nghĩa là:** XOR IV gốc với plaintext gốc, rồi XOR tiếp với plaintext mong muốn => ra IV mới.

    ```python
    from pwn import xor

    P0_original = b"admin=False;expi"   # 16 byte đầu của plaintext gốc
    P0_target   = b"admin=True;\x00\x00\x00\x00\x00"  # plaintext mong muốn

    # IV' = IV ⊕ P0_original ⊕ P0_target
    iv_new = xor(iv, P0_original, P0_target)
    ```

    > **Lưu ý:** Block 0 bị xáo trộn không ảnh hưởng gì vì server chỉ cần tìm `admin=True` trong toàn bộ cookie sau khi split bằng `;`. Phần `expiry=...` vẫn nguyên vẹn ở block 1 trở đi.

- **Bước 3 — Gửi cookie đã chỉnh lên server:**

    ```
    GET /flipping_cookie/check_admin/{ct}/{iv_new.hex()}/
    ```

- **Kết quả:**

    ![](assets/symmeric%20ciphers/12.png)

## **13. Lazy CBC**
### Given
- Server có 3 endpoint:

    ```python
    @chal.route('/lazy_cbc/encrypt/<plaintext>/')
    def encrypt(plaintext):
        plaintext = bytes.fromhex(plaintext)
        if len(plaintext) % 16 != 0:
            return {"error": "Data length must be multiple of 16"}
        cipher = AES.new(KEY, AES.MODE_CBC, KEY)   # IV = KEY
        encrypted = cipher.encrypt(plaintext)
        return {"ciphertext": encrypted.hex()}

    @chal.route('/lazy_cbc/receive/<ciphertext>/')
    def receive(ciphertext):
        ciphertext = bytes.fromhex(ciphertext)
        if len(ciphertext) % 16 != 0:
            return {"error": "Data length must be multiple of 16"}
        cipher = AES.new(KEY, AES.MODE_CBC, KEY)   # IV = KEY
        decrypted = cipher.decrypt(ciphertext)
        try:
            decrypted.decode()  # kiểm tra ASCII hợp lệ
        except UnicodeDecodeError:
            return {"error": "Invalid plaintext: " + decrypted.hex()}  # Lộ plaintext
        return {"success": "Your message has been received"}

    @chal.route('/lazy_cbc/get_flag/<key>/')
    def get_flag(key):
        key = bytes.fromhex(key)
        if key == KEY:
            return {"plaintext": FLAG.encode().hex()}
        return {"error": "invalid key"}
    ```

- Ba điểm quan trọng ta cần lưu ý:

    - `IV = KEY`: dev lười không tạo IV riêng

    - `receive` trả về **plaintext hex** khi gặp lỗi decode ASCII

    - `get_flag` trả về flag nếu ta cung cấp đúng key

### Goal
- Khôi phục `KEY`, sau đó gọi `get_flag(KEY)` để lấy flag.

### Solution
- **Ý tưởng:** Khai thác CBC với IV = KEY

    Công thức **CBC decrypt** cho từng block:

    $$P_i = \text{AES\_Decrypt}(C_i) \oplus C_{i-1}$$

    Với block đầu tiên dùng IV thay cho `C_{-1}`:

    $$P_0 = \text{AES\_Decrypt}(C_0) \oplus IV$$

    Vì `IV = KEY,` nếu ta tạo ciphertext đặc biệt để lộ `AES_Decrypt(C_0)`, ta có thể tính ngược ra KEY.

- **Bước 1 — Chuẩn bị plaintext và mã hóa:**

    Gửi plaintext gồm 2 block bất kỳ (ví dụ toàn `b"a"`):

    ```python
    plaintext = b"a" * 32   # 2 block × 16 byte
    ct = encrypt(plaintext.hex())
    # ct = C0 (32 hex) + C1 (32 hex)
    C0 = ct[:32]
    C1 = ct[32:]
    ```

    Lúc này quá trình encrypt CBC như sau:

    $$C_0 = \text{AES\_Encrypt}(P_0 \oplus IV) = \text{AES\_Encrypt}(P_0 \oplus KEY)$$

    $$C_1 = \text{AES\_Encrypt}(P_1 \oplus C_0)$$

- **Bước 2 — Tạo ciphertext bẫy:**

    Gửi lên `receive` ciphertext gồm 2 block: `C0` + `C0` (block 0 lặp lại làm block 1):

    ```python
    fake_ct = C0 + C0
    result = receive(fake_ct)
    ```

    Server decrypt `fake_ct`:

    $$P'_0 = \text{AES\_Decrypt}(C_0) \oplus IV = \text{AES\_Decrypt}(C_0) \oplus KEY$$

    $$P'_1 = \text{AES\_Decrypt}(C_0) \oplus C_0$$

    `P'_0` chính là plaintext gốc `P_0 = b"a" * 16` (ASCII hợp lệ).

    `P'_1` là `AES_Decrypt(C0) ⊕ C0`: gần như chắc chắn **không phải ASCII hợp lệ** (random bytes) => server trả lỗi và lộ `P'_1` dưới dạng **hex**:

    ```
    {"error": "Invalid plaintext: 6161...XXXXXXXXXXXXXXXX"}
    #                              ^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^
    #                              P'_0 (ascii ok)   P'_1 (lộ ra đây!)
    ```

- **Bước 3 — Tính KEY từ plaintext bị lộ:**

    Ta có:
    $$P'_1 = \text{AES\_Decrypt}(C_0) \oplus C_0$$

    Từ bước 1, ta cũng biết:
    $$P_0 = \text{AES\_Decrypt}(C_0) \oplus KEY \implies \text{AES\_Decrypt}(C_0) = P_0 \oplus KEY$$

    Thay vào:
    $$P'_1 = (P_0 \oplus KEY) \oplus C_0$$

    XOR hai vế với `P_0` và `C_0`:
    $$KEY = P'_1 \oplus P_0 \oplus C_0$$

    ```python
    from pwn import xor

    P0    = b"a" * 16                          # plaintext block 0 gốc ta đã gửi
    P1_leaked = bytes.fromhex(result[32:64])   # P'_1 lộ ra từ error message
    C0_bytes  = bytes.fromhex(C0)

    KEY = xor(P1_leaked, P0, C0_bytes)
    ```

- **Bước 4 — Dùng KEY để lấy flag:**

    ```python
    flag_hex = get_flag(KEY.hex())
    print(bytes.fromhex(flag_hex).decode())
    ```

- **Kết quả:**

    ![](assets/symmeric%20ciphers/13.png)

    > **Bài học:** IV phải là giá trị ngẫu nhiên, dùng một lần (nonce) — không được tái sử dụng, và tuyệt đối không dùng key làm IV. Khi IV = KEY, bất kỳ ai quan sát được plaintext/ciphertext đều có thể khôi phục key chỉ với vài phép XOR đơn giản.

## **14. Triple DES**
### Given

- Hệ thống sử dụng thuật toán Triple DES (3DES) ở chế độ ECB, nhưng bọc thêm một lớp IV tĩnh (được tạo ngẫu nhiên một lần duy nhất khi server khởi động) bằng phép XOR. Công thức mã hóa: $C = E_K(P \oplus IV) \oplus IV$.
- API cho phép ta cung cấp khóa $K$ tùy ý (16-byte) để mã hóa Flag hoặc mã hóa một chuỗi văn bản bất kỳ.

### Goal

Lợi dụng điểm yếu toán học trong thuật toán sinh khóa (Key Schedule) của DES để tạo ra tính chất "tự nghịch đảo" (involution), qua đó triệt tiêu hoàn toàn ảnh hưởng của IV chưa biết và khôi phục bản rõ (Flag).

### Solution

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

#### Kết quả:  `crypto{n0t_4ll_k3ys_4r3_g00d_k3ys}`


## **15. Symmetry**

### Given

Hệ thống sử dụng AES ở chế độ OFB (Output Feedback). Chế độ này biến một Block Cipher (như AES) thành một Stream Cipher.

### Goal

Lợi dụng tính "đối xứng" (Symmetry) của chế độ OFB để biến hàm mã hóa (encrypt) thành hàm giải mã (decrypt) và lấy cờ.

### Solution

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

#### Kết quả: `crypto{0fb_15_5ymm37r1c4l_!!!11!}`


## **16. Bean Counter**

### Given

- Chế độ CTR (Counter) hoạt động bằng cách mã hóa một bộ đếm (Counter/IV) liên tục tăng dần để tạo ra một dòng khóa giả ngẫu nhiên (Keystream). 
- Sau đó, Keystream sẽ được XOR với bản rõ (Plaintext) để tạo ra bản mã (Ciphertext). 

### Goal

- Lợi dụng việc bộ đếm bị "đóng băng", kết hợp với kỹ thuật Known Plaintext Attack (Tấn công dựa trên bản rõ đã biết) để khôi phục Keystream, từ đó giải mã toàn bộ bức ảnh chứa Flag.

### Solution

- Ta tính ngược lại Keystream cực kỳ dễ dàng:$$K_{stream} = C_0 \oplus P_0$$

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
#### Kết quả: `crypto{hex_bytes_beans}`

## **17. CTRIME**

### Given

- Hệ thống nén dữ liệu (ở đây là zlib) bằng cách tìm các chuỗi lặp lại và thay thế chúng bằng con trỏ ngắn hơn (thuật toán LZ77). 
- Do đó, dữ liệu có nhiều phần lặp lại sẽ có kích thước nén nhỏ hơn.
- Dữ kiện: Server ghép đoạn plaintext ta gửi vào cùng với FLAG, nén chúng lại bằng zlib.compress, rồi mới mã hóa bằng AES-CTR. AES-CTR là một Stream Cipher, nó bảo toàn nguyên vẹn độ dài của bản rõ sau khi mã hóa.

### Goal

Lợi dụng sự thay đổi kích thước của bản mã (Ciphertext) để đoán từng ký tự của Flag. Đây là dạng tấn công Side-Channel (Kênh kề) qua độ dài dữ liệu nén.

### Solution

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
#### Kết quả: `crypto{CRIME_571ll_p4y5}`


## **18. Logon Zero**

### Given

-  Chế độ AES-CFB8 (Cipher Feedback 8-bit) có một lỗ hổng toán học chết người khi khởi tạo. Nếu đầu vào toàn là byte \x00, có một xác suất $1/256$ mà toàn bộ quá trình mã hóa/giải mã sẽ sinh ra đầu ra cũng toàn là byte \x00.
- Server cung cấp 3 API: reset_connection (tạo lại khóa/IV mới), reset_password (nhận một token và giải mã nó bằng CFB8 để làm mật khẩu mới), và authenticate (kiểm tra mật khẩu).

### Goal 

- Lợi dụng điểm yếu của CFB8 để ép máy chủ đổi mật khẩu của admin thành một chuỗi toàn số $0$, sau đó đăng nhập bằng mật khẩu toàn số $0$ đó để lấy Flag.

### Solution

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
#### Kết quả: `crypto{Zerologon_Windows_CVE-2020-1472}`


## **19. Stream of Consciousness**

### Given

Chế độ CTR (Counter) biến Block Cipher thành Stream Cipher bằng cách mã hóa bộ đếm để tạo ra Keystream, sau đó XOR với Plaintext.

### Goal 

- Thực hiện cuộc tấn công Many-Time Pad (Keystream Reuse). Khi Keystream bị sử dụng lại, nếu ta XOR hai bản mã với nhau, Keystream sẽ tự triệt tiêu, để lại kết quả là XOR của hai bản rõ gốc:
$$C_1 \oplus C_2 = (P_1 \oplus K) \oplus (P_2 \oplus K) = P_1 \oplus P_2$$
- Nhiệm vụ là từ $P_1 \oplus P_2$ này, dùng một phần bản rõ đã biết (Known Plaintext - như chữ crypto{) để khôi phục các văn bản còn lại.

### Solution

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
#### Kết quả: `crypto{k3y57r34m_r3u53_15_f474l}`

## **20. Dancing Queen**

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
#### Kết quả: `crypto{M1x1n6_r0und5_4r3_1nv3r71bl3!}`

## **21. Oh SNAP**
### Given
* **Giao thức:** Server sử dụng thuật toán mã hóa **RC4**.
* **Cơ chế:** Khi bạn gửi một bản tin, server sẽ tạo một `Keystream` bằng cách kết hợp `IV` (3 byte bạn gửi lên) và `SECRET_KEY` (Flag).
* **Lỗ hổng:** Server trả về lỗi kèm theo giá trị byte đầu tiên của bản mã nếu lệnh gửi lên không hợp lệ. Điều này vô tình tiết lộ byte đầu tiên của `Keystream`.
    * `keystream[0] = ciphertext[0] ^ plaintext[0]`
    * Vì ta biết byte đầu của plaintext (lệnh gửi đi), ta lấy được byte đầu của keystream ứng với mỗi IV.

### Goal
* Sử dụng lỗ hổng **FMS Attack** để khôi phục từng byte của `SECRET_KEY` (Flag) thông qua việc gửi các IV đặc biệt.

### Solution

#### Lỗ hổng FMS Attack
RC4 có một điểm yếu: nếu ta biết một phần của khóa (các byte IV) và byte đầu tiên của keystream, ta có xác suất cao đoán được byte tiếp theo của khóa.


Công thức dự đoán byte thứ $a$ của khóa ($K[a]$):
$$K[a] \approx (S_{target}^{-1}[Z] - j - S[a+3]) \pmod{256}$$
Trong đó:
* $Z$ là byte đầu tiên của keystream.
* $S$ và $j$ là trạng thái của bộ sinh khóa sau khi đã xử lý các byte trước đó.

#### Các bước thực hiện
1.  **Thu thập dữ liệu:** Với mỗi byte Flag cần tìm (vị trí $a$):
    * Gửi các IV có dạng đặc biệt: `(a + 3, 255, X)` với $X$ chạy từ $0$ đến $255$.
    * Ghi lại byte đầu tiên của keystream từ thông báo lỗi của server.
2.  **Thống kê (Statistical Analysis):**
    * Với mỗi kết quả trả về, tính toán "ứng cử viên" cho byte Flag hiện tại.
    * Byte nào xuất hiện với tần suất cao nhất (thường là trên 5% số mẫu) sẽ là byte chính xác của Flag.
3.  **Lặp lại:** Sau khi tìm được byte $a$, dùng nó để tiếp tục tìm byte $a+1$.

### **4. Mã khai thác (Tóm tắt)**
Sử dụng script bạn đã cung cấp (`ohSNAP.py`):
* Gửi request đến `/send_cmd/00/{IV}/`.
* Trích xuất byte từ lỗi: `int(res["error"].split(": ")[1], 16)`.
* Giả lập 3 bước đầu của KSA với IV và các byte Flag đã biết để tìm $S$ và $j$.
* Dùng mảng `prob` để đếm số lần xuất hiện của các giá trị byte dự đoán.

---
``` python 
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
```
![](assets/symmeric%20ciphers/21.png)
`crypto{w1R3d_equ1v4l3nt_pr1v4cy?!}`

## **22. Pad Thai**
### Given
* **Giao thức:** Server sử dụng AES-CBC để mã hóa một tin nhắn ngẫu nhiên (`self.message`).
* **Tính năng:**
    1. `encrypt`: Trả về Ciphertext (IV + Encrypted Message).
    2. `unpad`: Nhận vào Ciphertext, giải mã và kiểm tra xem Padding (PKCS#7) có hợp lệ hay không. Đây chính là **Oracle**.
    3. `check`: Nếu bạn gửi đúng nội dung tin nhắn (`self.message`), server sẽ trả về Flag.
* **Lỗ hổng:** Server tiết lộ việc Padding có đúng hay không (`True/False`) mà không cần biết khóa.

### Goal
* Sử dụng lỗ hổng Padding Oracle để giải mã Ciphertext, lấy lại nội dung `message` gốc, sau đó dùng lệnh `check` để lấy Flag.

### Solution

#### **Nguyên lý Padding Oracle Attack**
Trong chế độ CBC, byte cuối của block Plaintext hiện tại ($P_i$) được tạo ra bởi:
$$P_i[k] = Decrypt(C_i)[k] \oplus C_{i-1}[k]$$
Bằng cách thay đổi IV hoặc block Ciphertext trước đó ($C_{i-1}$), ta có thể điều khiển giá trị của $P_i$. Nếu ta thử lần lượt các giá trị và Server báo "Padding hợp lệ", ta có thể suy ra giá trị trung gian ($Intermediate$) sau khi giải mã.



#### **Các bước thực hiện (Dựa trên code giải Pad Thai.py)**
1. **Lấy Ciphertext:** Gọi option `encrypt` để lấy chuỗi hex gồm 32 byte (16 byte IV + 16 byte Ciphertext của tin nhắn).
2. **Giải mã từng byte (từ phải sang trái):**
   * Giả sử cần tìm byte cuối cùng (index 15). Ta muốn $P[15]$ sau khi giải mã có giá trị là `0x01` (Padding hợp lệ cho 1 byte).
   * Ta thay đổi byte tương ứng trong IV gốc ($IV[15]$) bằng một giá trị `fake_IV[15]`.
   * Gửi chuỗi `fake_IV + C` tới server. Nếu server trả về `result: True`, ta tìm được giá trị trung gian:
     $$Intermediate[15] = fake\_IV[15] \oplus 0x01$$
   * Từ đó suy ra Plaintext gốc: $P[15] = Intermediate[15] \oplus IV_{gốc}[15]$.
3. **Mở rộng cho các byte tiếp theo:** Để tìm byte index 14, ta cần padding là `0x02 0x02`. Ta dùng $Intermediate[15]$ đã tìm được để cố định byte cuối là `0x02` và dò tìm byte 14.
4. **Gửi kết quả:** Sau khi giải mã đủ 16 byte, ta có `message`. Gửi tin nhắn này qua option `check` để nhận Flag.

### **4. Kết quả**
Chạy script `Pad Thai.py` của bạn, kết quả sẽ như sau:
* Khôi phục từng byte của message (ví dụ: `7a3...`).
* Sau khi có đủ chuỗi hex message, script gửi lệnh kiểm tra.
``` python
from pwn import *
import json
import time

# Danh sách ký tự hex để ưu tiên tìm kiếm (tăng tốc 10 lần)
HEX_CHARS = [ord(c) for c in "0123456789abcdef"]
SEARCH_SPACE = HEX_CHARS + [i for i in range(256) if i not in HEX_CHARS]

def get_connection():
    while True:
        try:
            r = remote('socket.cryptohack.org', 13421, level='error')
            r.recvline() # Bỏ banner chào mừng
            return r
        except:
            print("[!] Lỗi kết nối, thử lại sau 3s...")
            time.sleep(3)

conn = get_connection()

def oracle(ct_hex):
    global conn
    while True:
        try:
            conn.sendline(json.dumps({"option": "unpad", "ct": ct_hex}).encode())
            line = conn.recvline()
            if not line: raise EOFError
            return json.loads(line.decode())["result"]
        except:
            conn.close()
            conn = get_connection()

# 1. Lấy Ciphertext mục tiêu
conn.sendline(json.dumps({"option": "encrypt"}).encode())
ct_hex = json.loads(conn.recvline().decode())["ct"]
ct_bytes = bytes.fromhex(ct_hex)
iv = ct_bytes[:16]
# self.message.hex() có 32 ký tự -> 32 bytes ASCII -> Cần 2 blocks dữ liệu + 1 block padding
blocks = [ct_bytes[i:i+16] for i in range(16, len(ct_bytes), 16)]

# 2. Giải mã Padding Oracle
final_decrypted_bytes = []
prev_block = iv

print(f"[*] Ciphertext: {ct_hex}")

for b_idx, target_block in enumerate(blocks):
    print(f"\n[*] Giải khối {b_idx + 1}/{len(blocks)}...")
    intermediate = bytearray(16)
    block_pt = bytearray(16)
    
    for i in range(15, -1, -1):
        pad_val = 16 - i
        fake_iv = bytearray(16)
        
        # Thiết lập các byte đã giải mã để tạo padding mong muốn
        for k in range(i + 1, 16):
            fake_iv[k] = intermediate[k] ^ pad_val
            
        for val in SEARCH_SPACE:
            # Tính toán byte IV giả để sau giải mã byte tại i bằng pad_val
            # Giúp tìm ra trạng thái trung gian
            test_byte = val ^ pad_val ^ prev_block[i]
            fake_iv[i] = test_byte
            
            if oracle((fake_iv + target_block).hex()):
                # Kiểm tra tránh trường hợp pad=1 vô tình trùng pad=2,3...
                if pad_val == 1:
                    fake_iv[i-1] ^= 1
                    if not oracle((fake_iv + target_block).hex()):
                        continue
                
                intermediate[i] = test_byte ^ pad_val
                block_pt[i] = intermediate[i] ^ prev_block[i]
                print(f"    [+] Byte {i:02d}: {chr(block_pt[i])}")
                break
                
    final_decrypted_bytes.extend(block_pt)
    prev_block = target_block

# 3. Xử lý kết quả cuối cùng
full_plaintext = bytes(final_decrypted_bytes)
# Gỡ padding PKCS#7
pad_len = full_plaintext[-1]
if pad_len < 16:
    message = full_plaintext[:-pad_len].decode()
else:
    message = full_plaintext.decode() # Trường hợp hiếm không có pad block

print(f"\n[!] Message khôi phục: {message}")

# Gửi message để lấy Flag
conn.sendline(json.dumps({"option": "check", "message": message}).encode())
print(f"[*] Kết quả từ server: {conn.recvline().decode()}")
```

![](assets/symmeric%20ciphers/22.png)
#### Flag: `crypto{if_you_ask_enough_times_you_usually_get_what_you_want}`

## **23. The Good, The Pad, The Ugly**
### Given
* **Giao thức:** Vẫn là AES-CBC với lỗ hổng Padding Oracle qua hàm `unpad`.
* **Sự thay đổi (The Twist):** Oracle không còn trả về kết quả chính xác 100%. 
    * Nếu Padding **Sai**: Oracle thỉnh thoảng vẫn trả về `True` (do `rng.random() > 0.4`).
    * Nếu Padding **Đúng**: Oracle luôn trả về `True`.
    * Công thức của server: `return good | (rng.random() > 0.4)`
* **Giới hạn:** Bạn có tối đa 12,000 lượt truy vấn (`max_queries`).

### Goal
* Vượt qua lớp nhiễu để xác định chính xác đâu là kết quả `True` thực sự (do padding đúng) và đâu là `True` giả (do nhiễu ngẫu nhiên), từ đó giải mã message và lấy Flag.

### Solution

#### **Xử lý Oracle có nhiễu bằng Thống kê**
Vì một kết quả sai có xác suất 40% (0.4) trả về `True`, nhưng một kết quả đúng **luôn luôn** là `True` (xác suất 100%), ta có thể sử dụng phương pháp thử nghiệm lặp lại (Sampling):
* Nếu ta gửi cùng một Ciphertext nhiều lần:
    * Nếu Padding **Sai**: Xác suất cả $N$ lần đều trả về `True` là $0.4^N$. Với $N=20$, con số này cực nhỏ ($\approx 10^{-8}$), coi như bằng 0.
    * Nếu Padding **Đúng**: Xác suất cả $N$ lần đều trả về `True` là $1.0$ (chắc chắn).



#### **Các bước thực hiện (Dựa trên code The Good, The Pad, The Ugly.py)**
1. **Lấy Ciphertext:** Kết nối tới `socket.cryptohack.org 13422` và lấy IV + Ciphertext.
2. **Xây dựng hàm `check_padding` tin cậy:**
   * Gửi request trong một vòng lặp (ví dụ 20 lần).
   * Chỉ cần **một lần** duy nhất Server trả về `False`, ta kết luận ngay lập tức: **Padding Sai**.
   * Nếu sau 20 lần đều là `True`, ta kết luận: **Padding Đúng**.
3. **Giải mã:** Tiến hành giải mã từng byte như bài Padding Oracle cơ bản nhưng sử dụng hàm check đã qua bộ lọc ở trên.
4. **Tối ưu hóa:** Vì biết `message` được tạo từ `.hex()`, ta chỉ cần kiểm tra các ký tự trong tập `0-9, a-f`. Điều này giúp tiết kiệm số lượng query để không vượt quá giới hạn 12,000.
    ``` python
    from Crypto.Util.number import long_to_bytes, inverse

    e = 0x10001
    N, d = (21711308225346315542706844618441565741046498277716979943478360598053144971379956916575370343448988601905854572029635846626259487297950305231661109855854947494209135205589258643517961521594924368498672064293208230802441077390193682958095111922082677813175804775628884377724377647428385841831277059274172982280545237765559969228707506857561215268491024097063920337721783673060530181637161577401589126558556182546896783307370517275046522704047385786111489447064794210010802761708615907245523492585896286374996088089317826162798278528296206977900274431829829206103227171839270887476436899494428371323874689055690729986771, 2734411677251148030723138005716109733838866545375527602018255159319631026653190783670493107936401603981429171880504360560494771017246468702902647370954220312452541342858747590576273775107870450853533717116684326976263006435733382045807971890762018747729574021057430331778033982359184838159747331236538501849965329264774927607570410347019418407451937875684373454982306923178403161216817237890962651214718831954215200637651103907209347900857824722653217179548148145687181377220544864521808230122730967452981435355334932104265488075777638608041325256776275200067541533022527964743478554948792578057708522350812154888097)

    keys = [106979, 108533, 69557, 97117, 103231]

    enc_flag = 20304610279578186738172766224224793119885071262464464448863461184092225736054747976985179673905441502689126216282897704508745403799054734121583968853999791604281615154100736259131453424385364324630229671185343778172807262640709301838274824603101692485662726226902121105591137437331463201881264245562214012160875177167442010952439360623396658974413900469093836794752270399520074596329058725874834082188697377597949405779039139194196065364426213208345461407030771089787529200057105746584493554722790592530472869581310117300343461207750821737840042745530876391793484035024644475535353227851321505537398888106855012746117

    prod = 1
    for k in keys:
        prod *= k

    dd = inverse(prod, e*d-1)
    print(long_to_bytes(pow(enc_flag, dd, N)))
    ```
#### Kết quả: `crypto{even_a_faulty_oracle_leaks_all_information}`

## **24. Oracular Spectacular**




## **25. Paper Plane**
### Given
**Giao thức:** Sử dụng chế độ mã hóa **AES-IGE**.
**Đặc điểm IGE:** * Công thức mã hóa: $c_i = f_K(p_i \oplus c_{i-1}) \oplus p_{i-1}$
    * Công thức giải mã: $p_i = f_K^{-1}(c_i \oplus p_{i-1}) \oplus c_{i-1}$
    * Trong đó $p_0$ và $c_0$ đóng vai trò như các vector khởi tạo (IV).
* **Lỗ hổng:** Hàm `send_msg` thực hiện giải mã và kiểm tra padding PKCS#7. Nếu padding sai, nó trả về lỗi. Đây chính là một **Padding Oracle**.

### Goal
 Khai thác Padding Oracle trên chế độ IGE để giải mã Flag.

### Solution

#### **Nguyên lý Padding Oracle trên IGE**
Mặc dù IGE phức tạp hơn CBC, nhưng về cốt lõi, việc giải mã $p_i$ vẫn phụ thuộc vào giá trị của $p_{i-1}$ và $c_{i-1}$ mà ta có thể kiểm soát được.
Công thức giải mã block cuối cùng ($n$):
$$p_n = Decrypt_K(c_n \oplus p_{n-1}) \oplus c_{n-1}$$

Để thực hiện Padding Oracle, ta cần thay đổi giá trị của $c_{n-1}$ hoặc $p_{n-1}$ sao cho sau khi giải mã, byte cuối cùng của $p_n$ là `0x01` (padding hợp lệ). Trong challenge này, server cho phép ta gửi cả `m0` (tương ứng $p_0$) và `c0` (tương ứng $c_0$), điều này cho phép ta thao túng quá trình lan truyền lỗi của IGE.

#### **Các bước thực hiện (Dựa trên code giải Paperplane.py)**
1. **Lấy dữ liệu:** Gọi `encrypt_flag` để lấy `ciphertext`, `m0` ($p_0$) và `c0` ($c_0$).
2. **Dò tìm giá trị trung gian:**
    Ta tập trung vào block cuối cùng. Ta thay đổi 16 byte cuối của chuỗi dữ liệu (đóng vai trò là $c_{n-1}$ trong công thức) để quan sát phản hồi từ server.
    Khi server báo "không có lỗi", nghĩa là byte cuối đã được đưa về đúng định dạng padding.
    Ta tính toán giá trị XOR tương ứng để tìm ra $p_n$.
3. **Lan truyền ngược:** Vì IGE có tính chất "infinite garble", kết quả giải mã block sau phụ thuộc vào các block trước. Tuy nhiên, bằng cách điều chỉnh cặp $(m_0, c_0)$ gửi lên mỗi lần, ta có thể cô lập từng block để giải mã như CBC thông thường.

### **4. Kết quả**
Chạy script `Paperplane.py` sẽ thực hiện:
* Duyệt qua từng byte của flag từ cuối lên đầu.
* Với mỗi byte, thử 256 giá trị cho đến khi padding hợp lệ.
* Ghép các byte đã giải mã để thu được Flag hoàn chỉnh.
``` python 
import requests
from pwn import xor
from Crypto.Util.number import *

def encrypt_flag():
    url = 'https://aes.cryptohack.org/paper_plane/encrypt_flag/'
    r = requests.get(url).json()
    return bytes.fromhex(r['ciphertext']), bytes.fromhex(r["m0"]), bytes.fromhex(r["c0"])

def send_msg(ciphertext, m0, c0):
    url = 'https://aes.cryptohack.org/paper_plane/send_msg/'
    url += ciphertext.hex() + "/" + m0.hex() + "/" + c0.hex()
    r = requests.get(url).json()
    return  'error' not in r


def decrypt_block(ctt, m0, c0):
    plaintext = b""
    new_xor = b""
    for i in range(1, 17):
        tmp = c0[:16-i]
        for j in range(255, -1, -1):
            if len(plaintext) > 0:
                pad = long_to_bytes(i)*(i-1)
                send = tmp + long_to_bytes(j) + xor(pad, new_xor)
            else:
                send = tmp + long_to_bytes(j)
            if send_msg(ctt, m0, send):
                new_xor = xor(long_to_bytes(i),(j)) +new_xor
                plaintext = xor(xor(long_to_bytes(i),(j)), (c0[16-i:17-i])) + plaintext 
                print(plaintext)
                break
    return plaintext

ciphertext, m0, c0 = encrypt_flag()
print(c0.hex())
ciphertext1 = ciphertext[:16]
ciphertext2 = ciphertext[16:]

pt1 = decrypt_block(ciphertext1, m0, c0)
print("block1 done")
print(f"{pt1 = }")
pt2 = decrypt_block(ciphertext2, pt1, ciphertext1)

print("flag: " , pt1 + pt2 )
```
`crypto{h3ll0_t3l3gr4m}`



## **26. Forbidden Fruit**


## **27. Beatboxer**
### Given
* Một server cung cấp 2 dịch vụ: **Encrypt message** (mã hóa chuỗi bất kỳ) và **Encrypt flag**.
* Thuật toán mã hóa dựa trên cấu trúc **AES** nhưng có một thay đổi chí mạng: bảng **S-box** tiêu chuẩn bị thay thế bằng một bảng S-box mới.
* Bảng S-box này có tính chất **tuyến tính** (Linear): $S(x \oplus y) \oplus S(0) = (S(x) \oplus S(0)) \oplus (S(y) \oplus S(0))$.

### Goal
* Giải mã các khối ciphertext của flag để lấy nội dung bản rõ (Plaintext).

### Solution

#### **Phân tích lỗ hổng**
Trong AES tiêu chuẩn, S-box là thành phần phi tuyến duy nhất để chống lại các cuộc tấn công toán học. Tuy nhiên, ở bài này, hàm S-box đã bị "tuyến tính hóa".
Nếu ta gọi hàm mã hóa toàn phần là $E(P)$, ta có thể tách nó thành:
$$E(P) = L(P) \oplus E(0)$$
Trong đó:
* $E(0)$ là kết quả khi mã hóa một khối toàn bit $0$ (chứa toàn bộ ảnh hưởng của các Round Keys và hằng số Affine).
* $L(P)$ là một **hàm tuyến tính** thuần túy trên trường $GF(2)^{128}$.

#### **Các bước thực hiện**
1.  **Lấy hằng số:** Gửi block toàn không `00...00` để nhận về $C_0 = E(0)$.
2.  **Xây dựng ma trận:** Vì $L(P)$ là hàm tuyến tính, ta có thể biểu diễn nó dưới dạng một ma trận $M$ kích thước $128 \times 128$. Ta tìm các cột của ma trận bằng cách gửi 128 bản tin thử, mỗi bản tin chỉ bật duy nhất 1 bit (Basis vectors).
3.  **Loại bỏ hằng số:** Lấy ciphertext của flag ($C_{flag}$), thực hiện phép tính: $Target = C_{flag} \oplus C_0$. Lúc này $Target = L(P)$.
4.  **Giải hệ phương trình:** Ta có phương trình ma trận $M \cdot P = Target$. Sử dụng thuật toán **Gauss-Jordan** để giải hệ phương trình trên trường $GF(2)$ và tìm lại bản rõ $P$.
5.  **Ghép flag:** Lặp lại với từng block 16 bytes của flag để thu được kết quả cuối cùng.

``` python 
from pwn import remote
import json

# Định nghĩa bảng SBOX biến dị của đề bài
SBOX = (
    0x2a, 0x00, 0x7e, 0x54, 0x82, 0xa8, 0xd6, 0xfc, 0x61, 0x4b, 0x35, 0x1f, 0xc9, 0xe3, 0x9d, 0xb7,
    0xbc, 0x96, 0xe8, 0xc2, 0x14, 0x3e, 0x40, 0x6a, 0xf7, 0xdd, 0xa3, 0x89, 0x5f, 0x75, 0x0b, 0x21,
    0x1d, 0x37, 0x49, 0x63, 0xb5, 0x9f, 0xe1, 0xcb, 0x56, 0x7c, 0x02, 0x28, 0xfe, 0xd4, 0xaa, 0x80,
    0x8b, 0xa1, 0xdf, 0xf5, 0x23, 0x09, 0x77, 0x5d, 0xc0, 0xea, 0x94, 0xbe, 0x68, 0x42, 0x3c, 0x16,
    0x44, 0x6e, 0x10, 0x3a, 0xec, 0xc6, 0xb8, 0x92, 0x0f, 0x25, 0x5b, 0x71, 0xa7, 0x8d, 0xf3, 0xd9, 
    0xd2, 0xf8, 0x86, 0xac, 0x7a, 0x50, 0x2e, 0x04, 0x99, 0xb3, 0xcd, 0xe7, 0x31, 0x1b, 0x65, 0x4f,
    0x73, 0x59, 0x27, 0x0d, 0xdb, 0xf1, 0x8f, 0xa5, 0x38, 0x12, 0x6c, 0x46, 0x90, 0xba, 0xc4, 0xee,
    0xe5, 0xcf, 0xb1, 0x9b, 0x4d, 0x67, 0x19, 0x33, 0xae, 0x84, 0xfa, 0xd0, 0x06, 0x2c, 0x52, 0x78,
    0xf6, 0xdc, 0xa2, 0x88, 0x5e, 0x74, 0x0a, 0x20, 0xbd, 0x97, 0xe9, 0xc3, 0x15, 0x3f, 0x41, 0x6b,
    0x60, 0x4a, 0x34, 0x1e, 0xc8, 0xe2, 0x9c, 0xb6, 0x2b, 0x01, 0x7f, 0x55, 0x83, 0xa9, 0xd7, 0xfd,
    0xc1, 0xeb, 0x95, 0xbf, 0x69, 0x43, 0x3d, 0x17, 0x8a, 0xa0, 0xde, 0xf4, 0x22, 0x08, 0x76, 0x5c,
    0x57, 0x7d, 0x03, 0x29, 0xff, 0xd5, 0xab, 0x81, 0x1c, 0x36, 0x48, 0x62, 0xb4, 0x9e, 0xe0, 0xca,
    0x98, 0xb2, 0xcc, 0xe6, 0x30, 0x1a, 0x64, 0x4e, 0xd3, 0xf9, 0x87, 0xad, 0x7b, 0x51, 0x2f, 0x05,
    0x0e, 0x24, 0x5a, 0x70, 0xa6, 0x8c, 0xf2, 0xd8, 0x45, 0x6f, 0x11, 0x3b, 0xed, 0xc7, 0xb9, 0x93, 
    0xaf, 0x85, 0xfb, 0xd1, 0x07, 0x2d, 0x53, 0x79, 0xe4, 0xce, 0xb0, 0x9a, 0x4c, 0x66, 0x18, 0x32, 
    0x39, 0x13, 0x6d, 0x47, 0x91, 0xbb, 0xc5, 0xef, 0x72, 0x58, 0x26, 0x0c, 0xda, 0xf0, 0x8e, 0xa4
)

# Các bảng nhân trong trường Galois phục vụ MixColumns
GMUL2 = (
    0x00, 0x02, 0x04, 0x06, 0x08, 0x0a, 0x0c, 0x0e, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1a, 0x1c, 0x1e, 
    0x20, 0x22, 0x24, 0x26, 0x28, 0x2a, 0x2c, 0x2e, 0x30, 0x32, 0x34, 0x36, 0x38, 0x3a, 0x3c, 0x3e, 
    0x40, 0x42, 0x44, 0x46, 0x48, 0x4a, 0x4c, 0x4e, 0x50, 0x52, 0x54, 0x56, 0x58, 0x5a, 0x5c, 0x5e, 
    0x60, 0x62, 0x64, 0x66, 0x68, 0x6a, 0x6c, 0x6e, 0x70, 0x72, 0x74, 0x76, 0x78, 0x7a, 0x7c, 0x7e, 
    0x80, 0x82, 0x84, 0x86, 0x88, 0x8a, 0x8c, 0x8e, 0x90, 0x92, 0x94, 0x96, 0x98, 0x9a, 0x9c, 0x9e, 
    0xa0, 0xa2, 0xa4, 0xa6, 0xa8, 0xaa, 0xac, 0xae, 0xb0, 0xb2, 0xb4, 0xb6, 0xb8, 0xba, 0xbc, 0xbe, 
    0xc0, 0xc2, 0xc4, 0xc6, 0xc8, 0xca, 0xcc, 0xce, 0xd0, 0xd2, 0xd4, 0xd6, 0xd8, 0xda, 0xdc, 0xde, 
    0xe0, 0xe2, 0xe4, 0xe6, 0xe8, 0xea, 0xec, 0xee, 0xf0, 0xf2, 0xf4, 0xf6, 0xf8, 0xfa, 0xfc, 0xfe, 
    0x1b, 0x19, 0x1f, 0x1d, 0x13, 0x11, 0x17, 0x15, 0x0b, 0x09, 0x0f, 0x0d, 0x03, 0x01, 0x07, 0x05, 
    0x3b, 0x39, 0x3f, 0x3d, 0x33, 0x31, 0x37, 0x35, 0x2b, 0x29, 0x2f, 0x2d, 0x23, 0x21, 0x27, 0x25, 
    0x5b, 0x59, 0x5f, 0x5d, 0x53, 0x51, 0x57, 0x55, 0x4b, 0x49, 0x4f, 0x4d, 0x43, 0x41, 0x47, 0x45, 
    0x7b, 0x79, 0x7f, 0x7d, 0x73, 0x71, 0x77, 0x75, 0x6b, 0x69, 0x6f, 0x6d, 0x63, 0x61, 0x67, 0x65, 
    0x9b, 0x99, 0x9f, 0x9d, 0x93, 0x91, 0x97, 0x95, 0x8b, 0x89, 0x8f, 0x8d, 0x83, 0x81, 0x87, 0x85, 
    0xbb, 0xb9, 0xbf, 0xbd, 0xb3, 0xb1, 0xb7, 0xb5, 0xab, 0xa9, 0xaf, 0xad, 0xa3, 0xa1, 0xa7, 0xa5, 
    0xdb, 0xd9, 0xdf, 0xdd, 0xd3, 0xd1, 0xd7, 0xd5, 0xcb, 0xc9, 0xcf, 0xcd, 0xc3, 0xc1, 0xc7, 0xc5, 
    0xfb, 0xf9, 0xff, 0xfd, 0xf3, 0xf1, 0xf7, 0xf5, 0xeb, 0xe9, 0xef, 0xed, 0xe3, 0xe1, 0xe7, 0xe5
)

GMUL3 = (
    0x00, 0x03, 0x06, 0x05, 0x0c, 0x0f, 0x0a, 0x09, 0x18, 0x1b, 0x1e, 0x1d, 0x14, 0x17, 0x12, 0x11, 
    0x30, 0x33, 0x36, 0x35, 0x3c, 0x3f, 0x3a, 0x39, 0x28, 0x2b, 0x2e, 0x2d, 0x24, 0x27, 0x22, 0x21, 
    0x60, 0x63, 0x66, 0x65, 0x6c, 0x6f, 0x6a, 0x69, 0x78, 0x7b, 0x7e, 0x7d, 0x74, 0x77, 0x72, 0x71, 
    0x50, 0x53, 0x56, 0x55, 0x5c, 0x5f, 0x5a, 0x59, 0x48, 0x4b, 0x4e, 0x4d, 0x44, 0x47, 0x42, 0x41, 
    0xc0, 0xc3, 0xc6, 0xc5, 0xcc, 0xcf, 0xca, 0xc9, 0xd8, 0xdb, 0xde, 0xdd, 0xd4, 0xd7, 0xd2, 0xd1, 
    0xf0, 0xf3, 0xf6, 0xf5, 0xfc, 0xff, 0xfa, 0xf9, 0xe8, 0xeb, 0xee, 0xed, 0xe4, 0xe7, 0xe2, 0xe1, 
    0xa0, 0xa3, 0xa6, 0xa5, 0xac, 0xaf, 0xaa, 0xa9, 0xb8, 0xbb, 0xbe, 0xbd, 0xb4, 0xb7, 0xb2, 0xb1, 
    0x90, 0x93, 0x96, 0x95, 0x9c, 0x9f, 0x9a, 0x99, 0x88, 0x8b, 0x8e, 0x8d, 0x84, 0x87, 0x82, 0x81, 
    0x9b, 0x98, 0x9d, 0x9e, 0x97, 0x94, 0x91, 0x92, 0x83, 0x80, 0x85, 0x86, 0x8f, 0x8c, 0x89, 0x8a, 
    0xab, 0xa8, 0xad, 0xae, 0xa7, 0xa4, 0xa1, 0xa2, 0xb3, 0xb0, 0xb5, 0xb6, 0xbf, 0xbc, 0xb9, 0xba, 
    0xfb, 0xf8, 0xfd, 0xfe, 0xf7, 0xf4, 0xf1, 0xf2, 0xe3, 0xe0, 0xe5, 0xe6, 0xef, 0xec, 0xe9, 0xea, 
    0xcb, 0xc8, 0xcd, 0xce, 0xc7, 0xc4, 0xc1, 0xc2, 0xd3, 0xd0, 0xd5, 0xd6, 0xdf, 0xdc, 0xd9, 0xda, 
    0x5b, 0x58, 0x5d, 0x5e, 0x57, 0x54, 0x51, 0x52, 0x43, 0x40, 0x45, 0x46, 0x4f, 0x4c, 0x49, 0x4a, 
    0x6b, 0x68, 0x6d, 0x6e, 0x67, 0x64, 0x61, 0x62, 0x73, 0x70, 0x75, 0x76, 0x7f, 0x7c, 0x79, 0x7a, 
    0x3b, 0x38, 0x3d, 0x3e, 0x37, 0x34, 0x31, 0x32, 0x23, 0x20, 0x25, 0x26, 0x2f, 0x2c, 0x29, 0x2a, 
    0x0b, 0x08, 0x0d, 0x0e, 0x07, 0x04, 0x01, 0x02, 0x13, 0x10, 0x15, 0x16, 0x1f, 0x1c, 0x19, 0x1a
)

# Các hàm phụ trợ mô phỏng AES
def transpose(m):
    return [m[4 * j + i] for i in range(4) for j in range(4)]

def mix_columns(state):
    s = [0] * 16
    for i in range(4):
        s[i] = GMUL2[state[i]] ^ GMUL3[state[i + 4]] ^ state[i + 8] ^ state[i + 12]
        s[i + 4] = state[i] ^ GMUL2[state[i + 4]] ^ GMUL3[state[i + 8]] ^ state[i + 12]
        s[i + 8] = state[i] ^ state[i + 4] ^ GMUL2[state[i + 8]] ^ GMUL3[state[i + 12]]
        s[i + 12] = GMUL3[state[i]] ^ state[i + 4] ^ state[i + 8] ^ GMUL2[state[i + 12]]
    return s

def shift_rows(state):
    return [
        state[0], state[1], state[2], state[3],
        state[5], state[6], state[7], state[4],
        state[10], state[11], state[8], state[9],
        state[15], state[12], state[13], state[14]
    ]

def linear_sub_bytes(state):
    # Phần cốt lõi: Loại bỏ hằng số affine bằng cách XOR với S(0)
    return [SBOX[b] ^ SBOX[0] for b in state]

def linear_encrypt_block(plaintext):
    """Mô phỏng phần tuyến tính của bộ mã hóa (không có AddRoundKey)"""
    state = transpose([c for c in plaintext])
    for i in range(1, 10):
        state = linear_sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
    state = linear_sub_bytes(state)
    state = shift_rows(state)
    return transpose(state)

# Chuyển đổi bit/byte
def bytes_to_bits(data):
    bits = []
    for b in data:
        for i in range(7, -1, -1):
            bits.append((b >> i) & 1)
    return bits

def bits_to_bytes(bits):
    res = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i+j]
        res.append(byte)
    return bytes(res)

def get_linear_matrix():
    """Dựng ma trận biểu diễn hàm tuyến tính L(P)"""
    matrix = []
    for i in range(128):
        inp = [0]*16
        inp[i//8] = 1 << (7 - (i%8))
        out = linear_encrypt_block(inp)
        matrix.append(bytes_to_bits(out))
    # Chuyển vị để các cột trở thành cơ sở
    return [list(row) for row in zip(*matrix)]

def solve_gauss(A, b):
    """Giải hệ phương trình Ax = b trên GF(2) bằng khử Gauss-Jordan"""
    n = 128
    for i in range(n):
        A[i].append(b[i])
    
    pivot = 0
    for j in range(n):
        if pivot >= n: break
        for i in range(pivot, n):
            if A[i][j]:
                A[pivot], A[i] = A[i], A[pivot]
                break
        else: continue
        
        for i in range(n):
            if i != pivot and A[i][j]:
                for k in range(j, n + 1):
                    A[i][k] ^= A[pivot][k]
        pivot += 1
    return [row[n] for row in A]

# Kết nối và giải bài toán
r = remote('socket.cryptohack.org', 13406)
r.recvline()

# 1. Lấy C0 = E(0)
r.sendline(json.dumps({"option": "encrypt_message", "message": "00"*16}).encode())
c0 = bytes.fromhex(json.loads(r.recvline())['encrypted_message'])

# 2. Lấy C_flag
r.sendline(json.dumps({"option": "encrypt_flag"}).encode())
c_flag_hex = json.loads(r.recvline())['encrypted_flag']
c_flag = bytes.fromhex(c_flag_hex)

# 3. Tính toán ma trận tuyến tính
matrix = get_linear_matrix()

# 4. Giải từng block 16 bytes của flag
full_flag = b""
for i in range(0, len(c_flag), 16):
    block_c = c_flag[i:i+16]
    # Target = E(P) ^ E(0) = L(P)
    target = bytes([b1 ^ b2 for b1, b2 in zip(block_c, c0)])
    target_bits = bytes_to_bits(target)
    
    res_bits = solve_gauss([row[:] for row in matrix], target_bits)
    full_flag += bits_to_bytes(res_bits)

# In kết quả cuối cùng
print(f"[!] Flag: {full_flag.decode().strip(chr(12))}")
```

`crypto{5b0x_l1n34r17y_15_d35457r0u5}`