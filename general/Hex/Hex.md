> ### 2. HEX

> Given
- Hệ thập lục phân có thể được sử dụng theo cách này để biểu diễn các chuỗi ASCII. 
- Đầu tiên, mỗi chữ cái được chuyển đổi thành một số thứ tự theo bảng ASCII (như trong thử thách trước). 
- Sau đó, các số thập phân được chuyển đổi thành số cơ số 16, hay còn gọi là hệ thập lục phân. Các số này có thể được kết hợp với nhau thành một chuỗi thập lục phân dài.

> Goal 

- Một cờ được mã hóa dưới dạng chuỗi thập lục phân.
`63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d`
-  Giải mã chuỗi này trở lại thành byte để lấy cờ.

> Solution

Bài này ta sử dụng hàm `bytes.fromhex()` hàm này có thể được sử dụng để chuyển đổi hệ thập lục phân sang byte
```python
hex_string = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
flag = bytes.fromhex(hex_string).decode()
print(flag)

```

Chạy code ra được flag `crypto{You_will_be_working_with_hex_strings_a_lot}`
<img width="1107" height="145" alt="image" src="https://github.com/user-attachments/assets/682a7e93-154c-4664-983a-534c12603e5e" />

---
