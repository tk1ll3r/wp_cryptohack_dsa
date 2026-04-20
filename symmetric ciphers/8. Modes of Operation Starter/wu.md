### Given
- CryptoHack cung cấp cho chúng ta một giao diện API tại đường dẫn: https://aes.cryptohack.org/block_cipher_starter/.
  
- Hệ thống cung cấp mã nguồn tham khảo với hai  chính:

<div align="center">

| Hàm | Chức năng | Trả về |
| :--- | :--- | :--- |
| `encrypt_flag()` | Mã hóa Flag bí mật bằng AES. | Một chuỗi Hex chứa bản mã (`ciphertext`). |
| `decrypt(ciphertext)` | Giải mã một chuỗi Hex bản mã bất kỳ. | Một chuỗi Hex chứa bản rõ (`plaintext`). |

</div>

### Goal
- Vì Flag đã được mã hóa, ta cần sử dụng chức năng `decrypt` của hệ thống để giải mã bản mã mà chức năng `encrypt_flag` trả về.

### Solution
- Nhấn vào nút `encrypt_flag()`, ta sẽ nhận được một chuỗi Hex:

    ![alt text](<Screenshot 2026-04-19 174321.png>)

- Copy chuỗi đó và dán vào ô tham số của hàm decrypt(ciphertext), sau đó nhấn nút **Decrypt**. Kết quả trả về là một chuỗi Hex mới.

    ![alt text](<Screenshot 2026-04-19 174410.png>)

- Sử dụng HEX ENCODER/DECODER để giải mã.

    ![alt text](<Screenshot 2026-04-19 174516.png>)