
## **Broken RSA (100 pts)**
![alt text](image-17-1.png)
### **1. Given**
* [cite_start]Các thông số RSA tiêu chuẩn: $n$, $e = 16$, và ciphertext $ct$[cite: 1].
* [cite_start]Điểm bất thường: Số mũ công khai $e$ là một lũy thừa của 2 ($e = 2^4 = 16$), trong khi thông thường $e$ phải là số nguyên tố (thường là 65537)[cite: 1].
* Vì $e = 16$ không nguyên tố cùng nhau với $\phi(n)$ (do $\phi(n)$ luôn chẵn), nên số nghịch đảo $d$ không tồn tại theo cách thông thường.

### **2. Goal**
* Giải quyết vấn đề $GCD(e, \phi(n)) \neq 1$ để tìm lại tất cả các bản rõ $m$ khả thi và lọc ra Flag.

### **3. Solution**

#### **Phân tích lỗ hổng**
Trong RSA, nếu $GCD(e, \phi(n)) = g > 1$, phép toán khai căn bậc $e$ modulo $n$ sẽ cho ra nhiều kết quả khác nhau (tương tự như việc $x^2 = 4$ có hai nghiệm $2$ và $-2$). Ở đây $e = 16$, nghĩa là ta đang thực hiện khai căn bậc 16, có thể dẫn đến tối đa 16 nghiệm khác nhau (các căn đơn vị).

#### **Các bước thực hiện**
1.  **Xác định $\phi(n)$:** Vì không có thông tin về các thừa số của $n$, giả định $n$ là số nguyên tố để tính $\phi(n) = n - 1$. Thực tế, $n$ trong bài là một số nguyên tố lớn.
2.  **Xử lý tính nguyên tố cùng nhau:** * Loại bỏ các thừa số chung của $e$ và $\phi(n)$ để tạo ra $\phi_{coprime}$ sao cho $GCD(e, \phi_{coprime}) = 1$.
    * Tính $d = e^{-1} \pmod{\phi_{coprime}}$.
3.  **Tìm nghiệm cơ sở:** Tính một nghiệm $m_0 = ct^d \pmod n$. Đây là một trong những bản rõ tiềm năng thỏa mãn $m_0^e \equiv ct \pmod n$.
4.  **Tìm các căn đơn vị (Roots of Unity):** * Tìm các giá trị $r$ sao cho $r^e \equiv 1 \pmod n$. 
    * Các nghiệm này được tìm bằng cách tính $i^{\phi_{coprime}} \pmod n$ với các số nguyên $i$ nhỏ.
5.  **Khôi phục Flag:** * Nhân nghiệm cơ sở $m_0$ với từng căn đơn vị: $m = (m_0 \cdot r) \pmod n$.
    * Chuyển các giá trị $m$ thu được từ dạng số sang dạng bytes để tìm chuỗi có định dạng `crypto{...}`.
``` python 
import Crypto.Util.number as cun
from pprint import pprint

def roots_of_unity(e, phi, n, rounds=500):
    # Divide common factors of `phi` and `e` until they're coprime.
    phi_coprime = phi
    while cun.GCD(phi_coprime, e) != 1:
        phi_coprime //= cun.GCD(phi_coprime, e)

    # Don't know how many roots of unity there are, so just try and collect a bunch
    roots = set(pow(i, phi_coprime, n) for i in range(1, rounds))

    assert all(pow(root, e, n) == 1 for root in roots)
    return roots, phi_coprime

e = 16
n=27772857409875257529415990911214211975844307184430241451899407838750503024323367895540981606586709985980003435082116995888017731426634845808624796292507989171497629109450825818587383112280639037484593490692935998202437639626747133650990603333094513531505209954273004473567193235535061942991750932725808679249964667090723480397916715320876867803719301313440005075056481203859010490836599717523664197112053206745235908610484907715210436413015546671034478367679465233737115549451849810421017181842615880836253875862101545582922437858358265964489786463923280312860843031914516061327752183283528015684588796400861331354873
c = 11303174761894431146735697569489134747234975144162172162401674567273034831391936916397234068346115459134602443963604063679379285919302225719050193590179240191429612072131629779948379821039610415099784351073443218911356328815458050694493726951231241096695626477586428880220528001269746547018741237131741255022371957489462380305100634600499204435763201371188769446054925748151987175656677342779043435047048130599123081581036362712208692748034620245590448762406543804069935873123161582756799517226666835316588896306926659321054276507714414876684738121421124177324568084533020088172040422767194971217814466953837590498718

# Problem: e and phi are not coprime - d does not exist
phi = n-1 # there were no prime factors of n

# Find e'th roots of unity modulo n
roots, phi_coprime = roots_of_unity(e, phi, n)

# Use our `phi_coprime` to get one possible plaintext
d = pow(e, -1, phi_coprime)
m = pow(c, d, n)
assert pow(m, e, n) == c

# Use the roots of unity to get all other possible plaintexts
ms = [(m * root) % n for root in roots]
ms = [cun.long_to_bytes(m) for m in ms]
pprint(ms)

```
---
`crypto{m0dul4r_squ4r3_r00t}`