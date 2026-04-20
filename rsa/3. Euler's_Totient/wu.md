### Given
- Cho hai số nguyên tố:

    $$p = 857504083339712752489993810777$$

    $$q = 1029224947942998075080348647219$$

- **Euler's Totient** của $N = p \cdot q$ được tính bằng công thức:

    $$ϕ(N)=(p−1)(q−1)$$

    > **Tại sao lại là $(p - 1)(q - 1)$?**
    >
    > Euler's Totient $\phi(N)$ đếm các số nguyên dương nhỏ hơn $N$ và nguyên tố cùng nhau với $N$. 
    > 
    > Vì $N = p \cdot q$ (với $p, q$ là số nguyên tố), các số **không** nguyên tố cùng nhau với $N$ chỉ có thể là bội của $p$ hoặc bội của $q$. Áp dụng nguyên lý **bao hàm - loại trừ (inclusion-exclusion)**:
    > 
    > $$\phi(N) = N - (q + p - 1) = (p - 1)(q - 1)$$

### Goal
- Tính $ϕ(N)=(p−1)(q−1)$

### Solution
- **Code Python:**
    ```python
    p = 857504083339712752489993810777
    q = 1029224947942998075080348647219

    phi = (p - 1) * (q - 1)
    print(phi)
    ```

    > **Vai trò của $\phi(N)$ trong RSA:**
    > 
    > Private key $d$ được tính từ $\phi(N)$ bằng công thức:
    > $$d = e^{-1} \pmod{\phi(N)}$$
    > Đây là lý do RSA an toàn — nếu không biết $p, q$ thì không thể tính được $\phi(N)$, từ đó kẻ tấn công không thể tìm được số nghịch đảo $d$ để giải mã bản tin.

- **Kết quả:**

    ![alt text](image.png)