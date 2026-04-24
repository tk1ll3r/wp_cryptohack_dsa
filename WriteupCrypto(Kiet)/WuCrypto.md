# Introduction 
## Network Attacks
![alt text](image.png)
### 1. Phân tích thử thách
Mục tiêu: Kết nối tới server qua Socket, trao đổi dữ liệu bằng định dạng JSON để nhận Flag.

Địa chỉ server: socket.cryptohack.org port 11112.

Yêu cầu: Gửi một đối tượng JSON với key là "buy" và value là "flag".

### 2. Giải quyết vấn đề
Bài toán yêu cầu chúng ta thực hiện 3 bước chính:

Thiết lập kết nối TCP: Sử dụng thư viện mạng để kết nối tới IP/Port của server.

Định dạng dữ liệu JSON: Server không nhận văn bản thuần túy (plaintext) mà yêu cầu cấu trúc JSON: {"buy": "flag"}.

Xử lý phản hồi: Đọc dữ liệu trả về từ server để trích xuất chuỗi Flag.

Tại sao không dùng pwntools?
Mặc dù đề bài gợi ý dùng pwntools, nhưng thư viện này gặp lỗi khi cài đặt trên môi trường Windows (do phụ thuộc vào thư viện unicorn yêu cầu trình biên dịch C++). Vì vậy, phương pháp tối ưu và nhẹ nhàng nhất là sử dụng thư viện socket và json có sẵn trong Python.
### 3.Mã khai thác dựa vào file pwntools_example.py được cho 
```
import socket
import json

# Thông tin mục tiêu
HOST = "socket.cryptohack.org"
PORT = 11112

# Bước 1: Tạo kết nối Socket
# create_connection giúp tự động xử lý việc phân giải tên miền và kết nối TCP
s = socket.create_connection((HOST, PORT))
f = s.makefile('rw') # Tạo interface để đọc/ghi dễ dàng như thao tác với file

# Bước 2: Nhận thông báo chào mừng
# Server gửi 4 dòng giới thiệu, chúng ta cần đọc hết để làm sạch buffer
for _ in range(4):
    print(f.readline().strip())

# Bước 3: Gửi payload JSON
# Theo yêu cầu đề bài: {"buy": "flag"}
request = {"buy": "flag"}
payload = json.dumps(request) + '\n' # Chuyển dict thành chuỗi JSON và thêm ký tự xuống dòng
f.write(payload)
f.flush() # Đảm bảo dữ liệu được gửi đi ngay lập tức

# Bước 4: Nhận Flag
response = f.readline()
print("-" * 20)
print(f"Phản hồi từ Server: {response.strip()}")
print("-" * 20)

s.close()
```
### 4.Flag:
![alt text](image-1.png)
```
Welcome to netcat's flag shop!
What would you like to buy?
I only speak JSON, I hope that's ok.

Sending: {'buy': 'flag'}
--------------------
KẾT QUẢ:
{"flag": "crypto{sh0pp1ng_f0r_fl4g5}"}
```
```crypto{sh0pp1ng_f0r_fl4g5}```

# GENERAL
## Data Formats
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-5.png)
### 1. Phân tích thử thách
* **Mục tiêu:** Trích xuất giá trị số nguyên thập phân của số mũ bí mật (**private key $d$**) từ một file định dạng **.pem**.
* **Định dạng PEM:** Là một dạng "bao bì" (container) chứa dữ liệu đã được mã hóa **Base64**. Dữ liệu bên trong Base64 tuân theo cấu trúc **ASN.1** và được mã hóa bằng chuẩn **DER**.
* **Tệp tin cung cấp:** `privacy_enhanced_mail.pem` chứa một khóa RSA Private Key.

### 2. Giải pháp thực hiện
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
![alt text](image-6.png)
* **Flag:** `15682700288056331364787171045819973654991149949197959929860861228180021707316851924456205543665565810892674190059831330231436970914474774562714945620519144389785158908994181951348846017432506464163564960993784254153395406799101314760033445065193429592512349952020982932218524462341002102063435489318813316464511621736943938440710470694912336237680219746204595128959161800595216366237538296447335375818871952520026993102148328897083547184286493241191505953601668858941129790966909236941127851370202421135897091086763569884760099112291072056970636380417349019579768748054760104838790424708988260443926906673795975104689`

![alt text](image-4.png)

## CERTainly not
![alt text](image-7.png)
### 1. Phân tích thử thách
* **Mục tiêu:** Trích xuất giá trị **Modulus ($n$)** từ một chứng chỉ số RSA định dạng **DER**.
* **Định dạng DER (Distinguished Encoding Rules):** Là định dạng nhị phân thô của dữ liệu mật mã. Khác với PEM, DER không thể đọc bằng mắt thường (không có lớp vỏ Base64).
* **SSL Certificate:** Trong chứng chỉ này chứa Public Key, và chúng ta cần lấy phần số nguyên $n$ trong Public Key đó.

### 2. Giải pháp
Vì file cung cấp là `.der` (binary), chúng ta cần đọc file ở chế độ nhị phân (`rb`). Thư viện `PyCryptodome` hỗ trợ hàm `RSA.importKey()` rất mạnh mẽ, nó có thể tự động phân tích cấu trúc ASN.1 phức tạp của chứng chỉ X.509 để tìm ra Public Key bên trong.

#### Các bước thực hiện:
1. Đọc dữ liệu nhị phân từ file `2048b-rsa-example-cert.der`.
2. Sử dụng `RSA.importKey()` để tạo đối tượng khóa.
3. Truy xuất thuộc tính `.n` để lấy Modulus ở dạng số nguyên thập phân.

### 3. Mã khai thác (Exploit Script)

```python
from Crypto.PublicKey import RSA

# Đọc file định dạng nhị phân (DER)
with open("2048b-rsa-example-cert.der", "rb") as f:
    cert_data = f.read()

# Import chứng chỉ (thư viện tự tách Public Key bên trong)
key = RSA.importKey(cert_data)

# In ra giá trị n (Modulus)
print(key.n)
```

### 4. Kết quả
![alt text](image-9.png)
**Flag:** `22825373692019530804306212864609512775374171823993708516509897631547513634635856375624003737068034549047677999310941837454378829351398302382629658264078775456838626207507725494030600516872852306191255492926495965536379271875310457319107936020730050476235278671528265817571433919561175665096171189758406136453987966255236963782666066962654678464950075923060327358691356632908606498231755963567382339010985222623205586923466405809217426670333410014429905146941652293366212903733630083016398810887356019977409467374742266276267137547021576874204809506045914964491063393800499167416471949021995447722415959979785959569497`


![alt text](image-8.png)

## SSH Keys
