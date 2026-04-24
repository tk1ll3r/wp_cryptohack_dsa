# Introduction 
## Network Attacks
![alt text](image.png)
### 1. Given 
Mục tiêu: Kết nối tới server qua Socket, trao đổi dữ liệu bằng định dạng JSON để nhận Flag.

Địa chỉ server: socket.cryptohack.org port 11112.

Yêu cầu: Gửi một đối tượng JSON với key là "buy" và value là "flag".

### 2.Goal 
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