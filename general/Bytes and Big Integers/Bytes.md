> ### 4. Bytes and Big Integers

> Given
- Các hệ mật mã như RSA hoạt động trên các con số, nhưng thông điệp lại được tạo thành từ các ký tự. 
- Để chuyển đổi thông điệp thành các con số để có thể áp dụng các phép toán cách phổ biến nhất là lấy các byte thứ tự của thông điệp, chuyển đổi chúng thành hệ thập lục phân, rồi ghép nối lại.
- Kết quả có thể được hiểu là một số thập lục phân/cơ số 16, và cũng có thể được biểu diễn trong hệ thập phân/cơ số 10.

> Goal 

- Chuyển số nguyên hệ 10 thành bytes, rồi diễn giải bytes đó thành ký tự ASCII/text
`11515195063862318899931685488813747395775516287289682636499965282714637259206269`

> Solution

```python
n = 11515195063862318899931685488813747395775516287289682636499965282714637259206269

b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
print(b)
print(b.decode())
```

Chạy code ra được flag `crypto{3nc0d1n6_4ll_7h3_w4y_d0wn}`
<img width="1241" height="148" alt="image" src="https://github.com/user-attachments/assets/b58386d4-ccda-4561-9016-e735db6bb936" />

---
