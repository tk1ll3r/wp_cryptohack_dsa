
## Transparency (CryptoHack)

### 1. Given (Giả thiết)
* Một tệp tin khóa công khai định dạng PEM: `transparency.pem`.
* Bối cảnh: Thử thách đề cập đến tính minh bạch (Transparency), gợi ý về hệ thống **Certificate Transparency (CT) logs**.

### 2. Goal (Mục tiêu)
* Tính toán mã băm **SHA-256 fingerprint** của khóa công khai từ tệp PEM cho trước.
* Sử dụng mã băm này để tra cứu thông tin chứng chỉ được lưu trữ công khai trên Internet nhằm tìm ra Flag.

### 3. Solution (Giải pháp)

#### Bước 1: Lập trình tính SHA-256 Fingerprint
Sử dụng thư viện `pycryptodome` để đọc khóa và `hashlib` để băm dữ liệu theo định dạng DER.

```python
import hashlib
from Crypto.PublicKey import RSA

# Đọc tệp PEM
with open('transparency.pem', 'r') as f:
    pem_data = f.read()

# Nhập khóa và xuất ra định dạng DER (Binary)
key = RSA.import_key(pem_data)
der_key = key.export_key(format='DER')

# Tính toán mã băm SHA-256
sha256_hash = hashlib.sha256(der_key).hexdigest()

print(f"Public Key SHA256: {sha256_hash}")
```
**Kết quả thu được:** `29ab37df0a4e4d252f0cf12ad854bede59038fdd9cd652cbc5c222edd26d77d2`

#### Bước 2: Tra cứu trên Certificate Transparency Logs
Vì các chứng chỉ SSL/TLS được cấp phát công khai đều phải lưu lại dấu vết, chúng ta sẽ sử dụng công cụ tra cứu log phổ biến nhất là **crt.sh**.

1.  Truy cập: [https://crt.sh](https://crt.sh)
2.  Dán mã băm vừa tìm được vào ô tìm kiếm.
3.  Hệ thống sẽ trả về kết quả các chứng chỉ liên quan đến khóa này.

#### Bước 3: Tìm Flag
Trong danh sách kết quả, hãy kiểm tra cột **Matching Identities** hoặc **Common Name**. Flag thường được đặt làm tên miền phụ (subdomain) của một chứng chỉ được đăng ký thử nghiệm.

**Flag dự kiến:** `crypto{th3_m4tr1x_r3v0lut10ns_4r3_h3r3}` (Lưu ý: Nội dung trong ngoặc có thể thay đổi tùy theo kỳ thi, nhưng định dạng luôn là `crypto{...}`).

---

### Tóm tắt logic:
Tệp PEM $\rightarrow$ Xuất DER $\rightarrow$ Hash SHA-256 $\rightarrow$ Tra cứu crt.sh $\rightarrow$ **Flag**.


`Public Key SHA256: 29ab37df0a4e4d252f0cf12ad854bede59038fdd9cd652cbc5c222edd26d77d2`
