# GENERAL
## Data Formats
### 1.Given 
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-5.png)
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
![alt text](image-6.png)
* **Flag:** `15682700288056331364787171045819973654991149949197959929860861228180021707316851924456205543665565810892674190059831330231436970914474774562714945620519144389785158908994181951348846017432506464163564960993784254153395406799101314760033445065193429592512349952020982932218524462341002102063435489318813316464511621736943938440710470694912336237680219746204595128959161800595216366237538296447335375818871952520026993102148328897083547184286493241191505953601668858941129790966909236941127851370202421135897091086763569884760099112291072056970636380417349019579768748054760104838790424708988260443926906673795975104689`

![alt text](image-4.png)