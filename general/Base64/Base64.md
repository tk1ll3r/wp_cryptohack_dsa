> ### 3. BASE64

> Given
- Một lược đồ mã hóa phổ biến khác là Base64, cho phép chúng ta biểu diễn dữ liệu nhị phân dưới dạng chuỗi ASCII bằng bảng chữ cái gồm 64 ký tự. 
- Một ký tự của chuỗi Base64 mã hóa 6 chữ số nhị phân (bit), và do đó 4 ký tự Base64 mã hóa ba byte 8 bit.

> Goal 

- Hãy lấy chuỗi thập lục phân bên dưới, giải mã nó thành byte và sau đó mã hóa nó thành Base64.
`72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf`

> Solution

Bài này ta sử dụng base64.b64encode() trong python để giải mã chuỗi hex
```python
import base64

hex_string = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
raw_bytes = bytes.fromhex(hex_string)
encoded = base64.b64encode(raw_bytes)

print(encoded.decode())
```

Chạy code ra được flag `crypto/Base+64+Encoding+is+Web+Safe/`
<img width="1134" height="150" alt="image" src="https://github.com/user-attachments/assets/b2068234-35fa-4aab-85b1-dcac1f36f505" />

---
