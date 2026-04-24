from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import inverse

# 1. Thông số đã cho
p = 51894141255108267693828471848483688186015845988173648228318286999011443419469
q = 77342270837753916396402614215980760127245056504361515489809293852222206596161
n = p * q
e = 65537 # Thông thường e là 65537, nếu key.pem của bạn khác hãy sửa lại

# 2. Tính toán các thông số RSA
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

# 3. Khởi tạo Key RSA
# Sử dụng bộ (n, e, d, p, q) giúp thư viện xử lý nhanh và chính xác hơn
key_params = (n, e, d, p, q)
key = RSA.construct(key_params)

# 4. Dữ liệu bản mã (Ciphertext)
c_hex = "249d72cd1d287b1a15a3881f2bff5788bc4bf62c789f2df44d88aae805b54c9a94b8944c0ba798f70062b66160fee312b98879f1dd5d17b33095feb3c5830d28"
ciphertext = bytes.fromhex(c_hex)

# 5. Giải mã sử dụng PKCS1_OAEP
try:
    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(ciphertext)
    print("Nội dung giải mã (Flag):")
    print(plaintext.decode())
except ValueError as e:
    print(f"Lỗi giải mã: {e}")
    print("Có thể bản mã hoặc các số nguyên tố p, q không khớp với khóa.")