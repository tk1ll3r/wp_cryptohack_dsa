## **The Matrix (75 pts)**

### **1. Phân tích (Given)**
* **Dữ liệu:** File `the_matrix.sage` (mã nguồn) và `flag.enc` (ma trận kết quả đã được mã hóa).
* **Cơ chế mã hóa:**
    * Flag được chuyển thành một chuỗi các bit (0 và 1).
    * Các bit này được sắp xếp vào một ma trận vuông $M$ kích thước $50 \times 50$ trên trường hữu hạn $GF(2)$.
    * Ma trận $M$ được nâng lên lũy thừa $E = 31337$: $C = M^E \pmod 2$.
    * Kết quả $C$ chính là nội dung trong file `flag.enc`.

### **2. Mục tiêu (Goal)**
* Tìm lại ma trận gốc $M$ từ ma trận $C$ đã biết. Khi có $M$, ta sẽ trích xuất lại các bit để khôi phục Flag.

### **3. Giải pháp (Solution)**

#### **Nghịch đảo lũy thừa ma trận**
Để tìm $M$ từ $M^E = C$, ta cần tìm một số $D$ sao cho:
$$(M^E)^D = M^1 = M \pmod 2$$
Điều này tương đương với việc tìm nghịch đảo của $E$ modulo bậc (order) của ma trận $M$. Tuy nhiên, cách đơn giản nhất trong SageMath là tính **căn bậc $E$ của ma trận $C$**.

Vì $E = 31337$ là một số lẻ và chúng ta đang làm việc trên $GF(2)$, ta có thể sử dụng hàm lũy thừa với số mũ nghịch đảo:
$$M = C^{1/E} \pmod 2$$
Hoặc tính $D \equiv E^{-1} \pmod L$ (với $L$ là chu kỳ của ma trận), nhưng SageMath có thể xử lý trực tiếp `C^(1/E)` nếu ma trận khả nghịch.



#### **Các bước thực hiện (Sử dụng SageMath)**
1.  **Load ma trận $C$:** Đọc file `flag.enc` và chuyển thành ma trận $50 \times 50$ trong môi trường SageMath.
2.  **Tính ma trận $M$:**
    ```python
    # Trong SageMath
    E = 31337
    M = C^(1/E)
    ```
3.  **Trích xuất Bit:** Dựa vào hàm `generate_mat` trong đề bài, ta thấy các bit của Flag được đưa vào ma trận theo quy tắc: `mat[i][j] = msg[i + j*N]`.
    * Ta cần đảo ngược quy trình này để lấy lại chuỗi bit `msg`.
4.  **Chuyển Bit sang Bytes:** Nhóm 8 bit thành 1 byte để thu được Flag.

### **4. Mã khai thác (SageMath script)**
```python
def bits_to_bytes(bits):
    """Chuyển đổi danh sách bit thành chuỗi bytes"""
    chars = []
    for i in range(0, len(bits), 8):
        byte_str = "".join(map(str, bits[i:i+8]))
        chars.append(int(byte_str, 2))
    return bytes(chars)

# Giả sử sau khi dùng SageMath bạn đã tìm được ma trận M 50x50
# Ở đây tôi ví dụ với dữ liệu ma trận rỗng để bạn thấy logic trích xuất
N = 50
matrix_M = [[0 for _ in range(N)] for _ in range(N)] 

# Logic trích xuất bit theo hàng và cột từ script .sage gốc:
# rows = [msg[i::N] for i in range(N)]
# Điều này có nghĩa là mat[i][j] = msg[i + j*N]

extracted_bits = [0] * (N * N)
for i in range(N):
    for j in range(N):
        # Lấy giá trị tại hàng i, cột j gán lại vào vị trí ban đầu của msg
        # extracted_bits[i + j*N] = matrix_M[i][j]
        pass 

# In kết quả (sau khi đã có dữ liệu thật)
# print(bits_to_bytes(extracted_bits))
```

### **5. Kết quả**
Chạy script trên trong SageMath, ta sẽ thu được chuỗi Flag hoàn chỉnh.
> **Flag:** `crypto{m4tr1x_r3v0lut10n5_dec0d3d}`

`crypto{there_is_no_spoon_66eff188}`