### Given

- Một số định nghĩa:
    - **Quadratic Residue:** Một số nguyên $x$ được gọi là Quadratic Residue modulo $p$ nếu tồn tại số nguyên $a$ sao cho:
        $$a^2 ≡ x (mod p)$$
        Nói đơn giản: $x$ có căn bậc hai trong trường số modulo $p$.

    - **Quadratic Non-Residue:** Ngược lại — không tồn tại $a$ nào thỏa $a^2 ≡ x (mod p)$.

        Xấp xỉ một nửa các phần tử trong $\mathbb{F}_p^*$ là Non-Residue.

    - $\mathbb{F}_p^*$: Tập hợp các số nguyên từ $1$ đến $p−1$ trong trường hữu hạn modulo $p$ (không gồm 0).

- Cho Modulus: $p = 29$ (số nguyên tố)

- Danh sách cần kiểm tra:
    $$ints = [14, 6, 11]$$

### Goal
- Tìm phần tử nào trong $[14, 6, 11]$ là Quadratic Residue modulo $p=29$.

- Tính căn bậc hai của nó.

- Submit số nhỏ hơn trong hai nghiệm làm flag. Vì nếu $a^2 ≡ x (mod p)$ thì $(−a)^2 = a^2 ≡ x (mod p)$ cũng đúng. Hai nghiệm đó là $a$ và $p - a$

### Solution
- **Ý tưởng:** Brute-force kiểm tra từng phần tử

    Với mỗi $x$ trong danh sách, duyệt toàn bộ $a \in \lbrace 1, 2, ..., p-1 \rbrace$, kiểm tra xem có $a^2 ≡ x (mod p)$ không.

    ```python
    p = 29
    ints = [14, 6, 11]

    for x in ints:
        # Tìm tất cả a sao cho a^2 ≡ x (mod p)
        roots = [a for a in range(1, p) if pow(a, 2, p) == x]
        
        if roots:
            # x có căn bậc hai -> là Quadratic Residue
            print(f"{x} là Quadratic Residue, căn bậc hai: {roots}, nhỏ nhất: {min(roots)}")
        else:
            # x không có căn bậc hai -> là Quadratic Non-Residue
            print(f"{x} là Quadratic Non-Residue")
    ```

- **Kết quả:**

    ![](assets/) => zha tự sửa

    => Nghiệm submit: 8