### Given
- Một số nguyên tố 1024-bit: $p$

- Danh sách 10 số nguyên: $ints$

- Trong danh sách có 1 **Quadratic Residue** và 9 **Quadratic Non-Residue**.

- Điều kiện đặc biệt: $p ≡ 3 \pmod 4$

    > **Legendre Symbol:** Một công cụ toán học giúp kiểm tra nhanh xem một số có phải Quadratic Residue hay không, bằng một phép tính duy nhất:
    >
    > $$\left(\frac{a}{p}\right) \equiv a^{(p-1)/2} \pmod{p}$$
    >
    > * Kết quả = `1` $\rightarrow$ Quadratic Residue
    > * Kết quả = `p-1` $\rightarrow$ Quadratic Non-Residue
    > * Kết quả = `0` $\rightarrow$ a chia hết cho p

### Goal
- Dùng **Legendre Symbol** để tìm phần tử nào là Quadratic Residue trong danh sách $ints$.

- Tính căn bậc hai của nó modulo $p$.
  
- Submit `căn lớn hơn` trong hai nghiệm.

### Solution
- **Bước 1 — Dùng Legendre Symbol để lọc Quadratic Residue:**
  
    Với mỗi số $x$ trong $ints$, tính $x^{(p-1)/2} \pmod p$.
    
    Nếu kết quả bằng `1` thì $x$ là QR.

    ```python
    # Kiểm tra từng số bằng Legendre Symbol
    for x in ints:
        legendre = pow(x, (p - 1) // 2, p)
        if legendre == 1:
            qr = x  # Tìm thấy Quadratic Residue
    ```

- **Bước 2 — Tính căn bậc hai nhờ $p ≡ 3 \pmod4$:**
  
    Vì `p % 4 == 3`, ta có thể tận dụng **Fermat's Little Theorem** để tính căn trực tiếp:

    > **Fermat:** $a^{p-1} \equiv 1 \pmod p$, suy ra $a^{(p+1)/2} \equiv a^{1/2} \cdot a^{(p-1)/2} \equiv a^{1/2} \cdot 1 \pmod p$.
    > 
    > Khi $p \equiv 3 \pmod 4$, số $(p+1)/4$ là nguyên, nên:
    > 
    > $$\sqrt{x} \equiv x^{(p+1)/4} \pmod p$$

    ```python
    # Tính căn bậc hai bằng công thức Tonelli đơn giản khi p ≡ 3 mod 4
    root  = pow(qr, (p + 1) // 4, p)   # căn thứ nhất
    root2 = p - root                    # căn thứ hai (vì (-a)^2 = a^2)

    # Submit căn lớn hơn
    flag = max(root, root2)
    ```

- **Bước 3 — Kiểm chứng:**
    ```python
    assert pow(root, 2, p) == qr   # căn đúng
    assert pow(root2, 2, p) == qr  # căn kia cũng đúng
    ```

    Hai nghiệm thu được là `root` và `p - root`. Flag là nghiệm lớn hơn:

    ![alt text](image.png) => zha tự sửa

    > **Tại sao công thức này chỉ hoạt động khi $p \equiv 3 \pmod 4$?**
    >
    > Vì khi đó $(p+1)/4$ là số nguyên, nên phép mũ `pow(qr, (p+1)//4, p)` cho kết quả chính xác. Với các trường hợp tổng quát hơn (khi $p \equiv 1 \pmod 4$), cần dùng thuật toán **Tonelli-Shanks** phức tạp hơn.