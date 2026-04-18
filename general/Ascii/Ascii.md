> ## 1. ASCII

> ### Given
- ASCII là một chuẩn mã hóa 7 bit cho phép biểu diễn văn bản bằng các số nguyên từ 0 đến 127.

> ### Goal 

Sử dụng mảng số nguyên bên dưới, hãy chuyển đổi các số thành các ký tự ASCII tương ứng để thu được một cờ: (`[99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]`).

> ### Solution

Bài này ta sử dụng hàm `chr()` để chuyển đổi số thứ tự ASCII thành ký tự

```python
ascii_list = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]

s = ''.join(chr(x) for x in ascii_list)
print(s)

```

Chạy code ra được flag `cypto{ASCII_pr1nt4bl3}`

<img width="1089" height="147" alt="image" src="https://github.com/user-attachments/assets/5a0b5334-73b8-4f52-9c14-b176eccc3a2b" />

---
