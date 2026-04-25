Transparency


Đọc tệp PEM có tên “transparency.pem” chứa khóa công khai.
Nhập khóa và trích xuất khóa công khai.
Khóa công khai sau đó được xuất dưới định dạng DER.
Tính toán mã băm SHA-256 từ khóa công khai được mã hóa DER.
Cuối cùng, in ra SHA-256 của khóa công khai.


``` python 
import hashlib
from Crypto.PublicKey import RSA

pem = open('transparency.pem', 'r').read()
key = RSA.importKey(pem).public_key()

der = key.exportKey(format='DER')
sha256 = hashlib.sha256(der)
sha256_fingerprint = sha256.hexdigest()

print(f"Public Key SHA256: {sha256_fingerprint}")
```
`Public Key SHA256: 29ab37df0a4e4d252f0cf12ad854bede59038fdd9cd652cbc5c222edd26d77d2`