# **C. RSA**
## **1. Modular_Exponentiation**
### Given
- Challenge giới thiệu về **modular exponentiation** — phép tính nền tảng của RSA:
    $$base^{exponent} \pmod {modulus}$$

- Ví dụ: $2^{10} \pmod{17} = 1024 \pmod{17} = 4$

### Goal
- Tính kết quả của $101^{17} \pmod{22663}$

### Solution
- Dùng hàm `pow()` built-in của Python.

    Nhận 3 tham số `pow(base, exponent, modulus)` và tính modular exponentiation hiệu quả bằng thuật toán **fast exponentiation (square-and-multiply)** thay vì tính $101^{17}$ rồi mới mod (số sẽ rất lớn):

    ```python
    result = pow(101, 17, 22663)
    print(result)
    ```

    > Thuật toán square-and-multiply giữ số luôn nhỏ hơn n trong suốt quá trình tính, tránh overflow và chạy trong $O(log e)$ phép nhân thay vì $O(e)$.

- **Kết quả:**

   <img width="60" height="25" alt="image" src="https://github.com/user-attachments/assets/e041b011-2303-4f55-b084-892fbf8ba39f" />

   ---
## **2. Public_Keys**
  ### Given
- RSA encryption hoạt động như sau:

    $$C = M^e \pmod N \quad \text{với} \quad N = p \cdot q$$

- Các tham số cho trước:
    - Plaintext: $M = 12$

    - Exponent: $e = 65537$

    - Primes: $p = 17, q = 23$

    > **Public Key & Private Key trong RSA**
    >
    > * **Public key** gồm cặp $(N, e)$ — ai cũng biết.
    > * **Private key** là $d$ (modular inverse của $e \pmod{\phi(N)}$) — chỉ chủ sở hữu biết.
    > 
    > Việc tính $d$ từ $N$ mà không biết $p, q$ chính là bài toán **phân tích thừa số nguyên (integer factorization)** — một bài toán cực khó giúp tạo nên sự bảo mật của RSA.

### Goal
- Tính $12^{65537} \pmod {(17×23)}$

### Solution
- **Bước 1 - Tính modulus:**

    $$N = p × q$$

- **Bước 2: Mã hóa RSA:**

    $$C = M^e \pmod N$$

    ```python
    M = 12
    e = 65537
    p = 17
    q = 23

    # Bước 1: Tính modulus N = p × q
    N = p * q

    # Bước 2: Mã hóa RSA — C = M^e mod N
    C = pow(M, e, N)
    print(f"N = {N}")
    print(f"C = {C}")
    print(f"crypto{{{C}}}")
    ```

- **Kết quả:**

    <img width="83" height="48" alt="image" src="https://github.com/user-attachments/assets/35776f47-dc51-420e-87f9-c4f516b4d166" />


    > **Lưu ý về độ an toàn của RSA**
    >
    > RSA với $N = 391$ cực kỳ yếu — chỉ cần thử chia $391$ cho các số nguyên tố nhỏ là tìm được $p, q$ ngay ($391 = 17 \times 23$). 
    >
    > Trong thực tế, RSA thường sử dụng $N$ có kích thước **2048-bit** hoặc **4096-bit** để việc phân tích thừa số trở nên bất khả thi đối với cả những siêu máy tính mạnh nhất hiện nay.

---
## **3. Euler's_Totient**
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

   <img width="555" height="28" alt="image" src="https://github.com/user-attachments/assets/d318f059-0941-481a-8ac6-a38912a2a4b9" />


## **4. Private_Keys**
  ### Given
- Cho hai số nguyên tố và exponent public:
    $$p = 857504083339712752489993810777$$
    $$q = 1029224947942998075080348647219$$
    $$e = 65537$$

- Private key $d$ là **modular multiplicative inverse** của $e$ modulo $\phi(N)$:
    $$d \equiv e^{-1} \pmod{\phi(N)}$$

- Tức là $d$ thỏa mãn phương trình đồng dư:
    $$e \cdot d \equiv 1 \pmod{\phi(N)}$$

    > **Modular Multiplicative Inverse:** $d$ là số mà khi nhân với $e$ cho ra phần dư $1$ khi chia cho $\phi(N)$. Giá trị $d$ tồn tại khi và chỉ khi $\gcd(e, \phi(N)) = 1$. Trong giao thức RSA, điều này luôn được đảm bảo vì $e$ được chọn sao cho nguyên tố cùng nhau với $\phi(N)$. Ta có thể tìm $d$ hiệu quả bằng cách sử dụng **Thuật toán Euclid mở rộng (Extended Euclidean Algorithm**).

### Goal
- Tính $d \equiv e^{-1} \pmod{\phi(N)}$

### Solution
- **Bước 1 - Tính $\phi(N) = (p-1)(q-1)$:**

    ```python
    phi = (p - 1) * (q - 1)
    ```

- **Bước 2: Tính private key $d \equiv e^{-1} \pmod{\phi(N)}$:**

    ```python
    d = pow(e, -1, phi)
    ```

- **Kết quả:**

   <img width="553" height="25" alt="image" src="https://github.com/user-attachments/assets/c904c1a8-3403-4451-bac1-c3ae2476b959" />

    > #### **Tóm tắt RSA Keypair**
    >
    > * **Public key:** $(N, e)$ — dùng để **encrypt** (mã hóa).
    > * **Private key:** $d$ — dùng để **decrypt** (giải mã) theo công thức:
    >   $$M = C^d \pmod N$$
    >
    > **Điểm mấu chốt:** Nếu kẻ tấn công biết được $p$ và $q$, chúng có thể dễ dàng tính lại $\phi(N)$ rồi từ đó tìm ra $d$. Đây chính là lý do vì sao việc ngăn chặn **phân tích thừa số nguyên $N$** được coi là "trái tim" của toàn bộ hệ thống bảo mật RSA.

---

## **5. RSA Decryption**
### Given
- Các tham số RSA:
    - $N = 882564595536224140639625987659416029426239230804614613279163$

    - $e = 65537$

    - Ciphertext: $c = 77578995801157823671636298847186723593814843845525223303932$

- Private key $d$ đã tính ở challenge trước:
    $$d = 121832886702415731577073962957377780195510499965398469843281$$

### Goal
- Giải mã ciphertext $c$ bằng private key $d$ theo công thức RSA decrypt:
    $$M = c^d \pmod N$$

### Solution
- Vì RSA decrypt là phép tính đối xứng với encrypt nên thay vì dùng $e$, ta dùng $d$:

    $$ \text{Encrypt: } C = M^e \pmod N $$

    $$ \text{Decrypt: } M = C^d \pmod N $$

- Điều này đúng vì $e \cdot d \equiv 1 \pmod{\phi(N)}$, nên:

    $$ C^d = (M^e)^d = M^{e \cdot d} \equiv M^1 = M \pmod N $$

- **Code Python:**

    ```python
    # Các tham số RSA
    N = 882564595536224140639625987659416029426239230804614613279163
    e = 65537
    c = 77578995801157823671636298847186723593814843845525223303932

    # Private key từ challenge trước
    p = 857504083339712752489993810777
    q = 1029224947942998075080348647219
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)

    # Giải mã: M = c^d mod N
    M = pow(c, d, N)
    print(M)
    ```
- **Kết quả:**

  <img width="93" height="27" alt="image" src="https://github.com/user-attachments/assets/b3237cf3-6588-40b9-9cd9-3ed17222aa09" />

  ---
## **6. RSA Signatures**
 ### Given
- Challenge cung cấp file `private.key` chứa RSA private key, và yêu cầu *ký số* (digital signature) lên `message = "crypto{Immut4ble_m3ssag1ng}"`.

- Công thức ký số RSA:
    $$S=H(m)^d \pmod N$$

    Trong đó:

    - $H(m)$ = SHA256 hash của message, chuyển sang số nguyên

    - $d,N$ = private key lấy từ file `private.key`

    > **Digital Signature:** Thay vì encrypt bằng public key của người nhận, ta "encrypt" hash của message bằng private key của chính mình. Bất kỳ ai có public key của ta đều có thể verify bằng cách decrypt chữ ký và so sánh với hash của message. Nếu khớp -> message chưa bị chỉnh sửa và chắc chắn do ta gửi.

### Goal
- Đọc private key từ file `private.key`

- Tính SHA256 hash của message, chuyển sang số nguyên

- Ký số: $S=H(m)^d \pmod N$

### Solution
- **Bước 1 — Đọc private key từ file:**

    File `private.key` ở challenge này không phải PEM chuẩn mà là định dạng text thuần túy dạng `tên = giá trị` nên ta parse thủ công từng dòng:

    ```python
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    key_path    = os.path.join(current_dir, "private.key")

    with open(key_path, "rb") as f:
        key_text = f.read().decode("utf-8")

    # Đọc từng dòng, split theo "=" để lấy tên và giá trị
    values = {}
    for line in key_text.splitlines():
        name, value = line.split("=", 1)
        values[name.strip()] = int(value.strip())

    N = values["N"]
    d = values["d"]
    ```

- **Bước 2 — Tính SHA256 hash và chuyển sang số nguyên:**

    ```python
    from hashlib import sha256
    from Crypto.Util.number import bytes_to_long

    message = b"crypto{Immut4ble_m3ssag1ng}"

    # SHA256 → 32 bytes → số nguyên (big-endian)
    H = bytes_to_long(sha256(message).digest())
    ```

- **Bước 3 — Ký số và in kết quả:**

    ```python
    # S = H(m)^d mod N
    S = pow(H, d, N)
    print(S)
    ```

- **Kết quả:**

   <img width="1298" height="111" alt="image" src="https://github.com/user-attachments/assets/d269d16b-6c0c-498b-9547-f37403156570" />


    > **Tại sao ký lên hash thay vì ký trực tiếp lên message?** Vì $m$ có thể dài tùy ý, trong khi RSA chỉ hoạt động trên số nguyên nhỏ hơn $N$. SHA256 luôn cho ra output 256-bit cố định, phù hợp để đưa vào phép tính RSA. Ngoài ra, hash còn đảm bảo tính **collision resistance** — kẻ tấn công không thể tạo message khác có cùng hash.


## **7. Factoring**

### Given
- Hệ mật mã RSA hoạt động dựa trên một module $N$ được tạo ra bằng cách nhân hai số nguyên tố bí mật $p$ và $q$ ($N = p \cdot q$). Tính bảo mật của RSA phụ thuộc hoàn toàn vào việc máy tính rất khó để phân tích $N$ ngược lại thành $p$ và $q$ nếu module đó đủ lớn.
- Hệ thống cung cấp một module $N$ có kích thước khá nhỏ (150-bit):
$N = 510143758735509025530880200653196460532653147$

### Goal

Phân tích module $N$ thành hai thừa số nguyên tố $p$ và $q$. Cờ (Flag) chính là số nguyên tố có giá trị nhỏ hơn.

### Solution

Sử dụng các công cụ trực tuyến để phân tích, ở bài này mình sử dụng `FactorDB.com` để tìm ra được só o nguyên tố.
<img width="1889" height="460" alt="image" src="https://github.com/user-attachments/assets/05e0e94c-6c85-414e-a818-ac1a606ab340" />

> Và kết quả được mình lấy từ trang web: 
`19704762736204164635843`
 

## **8. Inferius Prime**

### Given
- Cơ sở: Độ an toàn của hệ mật mã công khai RSA phụ thuộc hoàn toàn vào độ phức tạp tính toán của bài toán phân tích nhân tử số nguyên lớn (Integer Factorization Problem - IFP). Theo các tiêu chuẩn an toàn thông tin hiện hành, module $N$ đòi hỏi kích thước tối thiểu từ 2048-bit để chống lại các kỹ thuật phân tích hiện đại.
- Hệ thống cung cấp cấu hình khóa công khai bao gồm số mũ $e = 65537$, bản mã $ct$ và module $N$. Phân tích thực nghiệm cho thấy module $N$ chỉ sở hữu xấp xỉ 60 chữ số thập phân (tương đương với không gian khoảng 200-bit). Sự sai lệch tham số này là một điểm yếu nghiêm trọng trong khâu khởi tạo, làm suy giảm hoàn toàn tính an toàn của hệ mật mã.

### Goal

Phân tích module $N$ thành 2 số nguyên tố $p$ và $q$. Sau đó, sử dụng $p$ và $q$ để tính khóa bí mật $d$ và giải mã ciphertext $ct$ về dạng văn bản (Flag).

### Solution

1. Sử dụng `FactorDB.com` phân tích thành 2 số p và q.
2. Tính số Euler Totient: $\phi = (p-1) \cdot (q-1)$.
3. Tính khóa bí mật $d$ bằng nghịch đảo modulo: $d \equiv e^{-1} \pmod \phi$.
4. Giải mã: $m = ct^d \pmod N$.
5. Dùng hàm `long_to_bytes` để chuyển số nguyên $m$ thành chuỗi Flag có thể đọc được.



```python
from Crypto.Util.number import long_to_bytes
n = 742449129124467073921545687640895127535705902454369756401331
e = 3 
ct = 39207274348578481322317340648475596807303160111338236677373
p =  752708788837165590355094155871
q =  986369682585281993933185289261
phi = (p-1)*(q-1)
d = pow(e,-1,phi) #decryption key 

decrypt = pow(ct,d,n)

print(long_to_bytes(decrypt))

```


> Kết quả: 
`b'crypto{N33d_b1g_pR1m35}'`

 
## **9. Monoprime**

### Given

- Trong hệ mật mã RSA tiêu chuẩn, module $N$ được thiết lập từ tích của hai số nguyên tố phân biệt ($N = p \cdot q$). Dựa trên đặc tính này, phi hàm Euler (Euler's Totient function) được tính bằng công thức $\phi(N) = (p-1)(q-1)$.
- Tuy nhiên, hệ thống "Monoprime" này mắc một lỗi thiết kế kiến trúc cơ bản: module $N$ được cấu tạo từ một số nguyên tố duy nhất ($N = p$). Sự biến đổi này phá vỡ hoàn toàn bài toán phân tích nhân tử, vốn là nền tảng bảo mật của RSA.
- Bài toán cung cấp bộ tham số khóa công khai gồm số mũ $e = 65537$, bản mã $ct$ và một module $N$ siêu lớn nhưng bản thân nó đã là một số nguyên tố.
### Goal

- Khai thác lỗ hổng cấu trúc của module $N$ để tính toán trực tiếp phi hàm Euler $\phi(N)$, qua đó suy xuất khóa giải mã bí mật $d$ và khôi phục bản mã $ct$ về định dạng văn bản (Flag).

### Solution

- Khi module $N$ là một số nguyên tố, ta không cần phải dùng bất kỳ công cụ nào để phân tích (factorize) nó nữa. 
- Dựa theo định nghĩa toán học của phi hàm Euler, số lượng các số nguyên tố cùng nhau với một số nguyên tố $N$ chính là $N - 1$.Do đó, công thức tính $\phi$ được đơn giản hóa tối đa:$$\phi(N) = N - 1$$

```python
from Crypto.Util.number import long_to_bytes
n = 171731371218065444125482536302245915415603318380280392385291836472299752747934607246477508507827284075763910264995326010251268493630501989810855418416643352631102434317900028697993224868629935657273062472544675693365930943308086634291936846505861203914449338007760990051788980485462592823446469606824421932591
e = 65537 
ct = 161367550346730604451454756189028938964941280347662098798775466019463375610700074840105776873791605070092554650190486030367121011578171525759600774739890458414593857709994072516290998135846956596662071379067305011746842247628316996977338024343628757374524136260758515864509435302781735938531030576289086798942

p = 1 
q = n
phi = (q-1)
d = pow(e,-1,phi)
decrypt = pow(ct,d,n)
print(long_to_bytes(decrypt))
```


> Ra được kết quả: 
`b'crypto{0n3_pr1m3_41n7_pr1m3_l0l}'`


## **10. Square Eyes**

### Given
- Trong quá trình sinh khóa RSA tiêu chuẩn, module $N$ bắt buộc phải là tích của hai số nguyên tố phân biệt ($N = p \cdot q$). 
- Dựa trên định lý cơ bản của số học, phi hàm Euler cho cấu trúc này là $\phi(N) = (p-1)(q-1)$. 
- Tuy nhiên, ở bài toán này, kiến trúc hệ thống đã bị thay đổi: module $N$ được thiết lập bằng bình phương của một số nguyên tố duy nhất ($N = p^2$). Khi cấu trúc vi phạm quy tắc này, công thức tính phi hàm Euler thay đổi. 
- Theo định lý toán học đối với lũy thừa của một số nguyên tố $p^k$, ta có $\phi(p^k) = p^k - p^{k-1}$. Do đó, với $k=2$, phi hàm được xác định bằng: $\phi(N) = p^2 - p = p(p-1)$.
- Hệ thống cung cấp bản mã $ct$, số mũ $e = 65537$ và một module $N$ khổng lồ (khoảng 4096-bit). Tác giả xác nhận rằng $N$ được tạo ra bằng cách lấy một số nguyên tố 2048-bit và "nhân nó với chính nó" (dùng hai lần).

### Goal

- Khai thác điểm yếu cấu trúc của module $N = p^2$ bằng thuật toán khai căn bậc hai số nguyên (Integer Square Root) để tìm lại tham số $p$. 
- Sau đó, áp dụng đúng định lý phi hàm Euler cho lũy thừa số nguyên tố để tính toán khóa giải mã $d$ và khôi phục văn bản gốc.

### Solution

- Dựa trên gợi ý của đề bài về phi hàm Euler, ta xác định được module $N$ là một số chính phương ($N = p^2$, đồng nghĩa $p = q$). 
- Do đó, ta có thể dễ dàng tìm $p$ bằng phép khai căn bậc hai ($p = \sqrt{N}$) và tính phi hàm theo công thức: $\phi(N) = p \cdot (p-1)$.

```python
from Crypto.Util.number import long_to_bytes, inverse

n = 535860808044009550029177135708168016201451343147313565371014459027743491739422885443084705720731409713775527993719682583669164873806842043288439828071789970694759080842162253955259590552283047728782812946845160334801782088068154453021936721710269050985805054692096738777321796153384024897615594493453068138341203673749514094546000253631902991617197847584519694152122765406982133526594928685232381934742152195861380221224370858128736975959176861651044370378539093990198336298572944512738570839396588590096813217791191895941380464803377602779240663133834952329316862399581950590588006371221334128215409197603236942597674756728212232134056562716399155080108881105952768189193728827484667349378091100068224404684701674782399200373192433062767622841264055426035349769018117299620554803902490432339600566432246795818167460916180647394169157647245603555692735630862148715428791242764799469896924753470539857080767170052783918273180304835318388177089674231640910337743789750979216202573226794240332797892868276309400253925932223895530714169648116569013581643192341931800785254715083294526325980247219218364118877864892068185905587410977152737936310734712276956663192182487672474651103240004173381041237906849437490609652395748868434296753449
e = 65537
ct = 222502885974182429500948389840563415291534726891354573907329512556439632810921927905220486727807436668035929302442754225952786602492250448020341217733646472982286222338860566076161977786095675944552232391481278782019346283900959677167026636830252067048759720251671811058647569724495547940966885025629807079171218371644528053562232396674283745310132242492367274184667845174514466834132589971388067076980563188513333661165819462428837210575342101036356974189393390097403614434491507672459254969638032776897417674577487775755539964915035731988499983726435005007850876000232292458554577437739427313453671492956668188219600633325930981748162455965093222648173134777571527681591366164711307355510889316052064146089646772869610726671696699221157985834325663661400034831442431209123478778078255846830522226390964119818784903330200488705212765569163495571851459355520398928214206285080883954881888668509262455490889283862560453598662919522224935145694435885396500780651530829377030371611921181207362217397805303962112100190783763061909945889717878397740711340114311597934724670601992737526668932871436226135393872881664511222789565256059138002651403875484920711316522536260604255269532161594824301047729082877262812899724246757871448545439896

p = q = 23148667521998097720857168827790771337662483716348435477360567409355026169165934446949809664595523770853897203103759106983985113264049057416908191166720008503275951625738975666019029172377653170602440373579593292576530667773951407647222757756437867216095193174201323278896027294517792607881861855264600525772460745259440301156930943255240915685718552334192230264780355799179037816026330705422484000086542362084006958158550346395941862383925942033730030004606360308379776255436206440529441711859246811586652746028418496020145441513037535475380962562108920699929022900677901988508936509354385660735694568216631382653107
# print(p)
phi = (p-1)*(q)
d = pow(e,-1,phi)

decrypt = pow(ct,d,n)
print(long_to_bytes(decrypt))
```

> Kết quả:
`b'crypto{squar3_r00t_i5_f4st3r_th4n_f4ct0r1ng!}`


## **11. ManyPrime**

### Given
Bài toán cung cấp ba giá trị `n`, `e` và `ct` trong một hệ thống RSA, trong đó `n` là tích của nhiều số nguyên tố nhỏ.

#### Tham số
- **n**: Một số lớn là tích của nhiều số nguyên tố.
- **e**: Số mũ công khai (`e = 65537`).
- **ct**: Dữ liệu mã hóa (ciphertext) cần giải mã.

### Goal
Bài toán này dựa trên **RSA đa nguyên tố** (multi-prime RSA), trong đó `n` không phải là tích của chỉ hai số nguyên tố (như trong RSA chuẩn), mà là tích của nhiều số nguyên tố nhỏ. Với bài toán như vậy, **Phương pháp Eliptic Curve (ECM)** là một kỹ thuật hữu ích để phân tích số liệu.

### Solution

#### 1. Phân tích số `n`
Vì `n` là tích của nhiều số nguyên tố, chúng ta sử dụng **Phương pháp ECM** để phân tích `n`. Mục tiêu là tìm ra các yếu tố nguyên tố `p1, p2, ..., pk` sao cho:
\[
n = p1 \times p2 \times \cdots \times pk
\]

#### 2. Tính hàm Euler `φ(n)`
Khi đã có được các yếu tố nguyên tố, ta có thể tính hàm Euler `φ(n)`:
\[
φ(n) = (p1 - 1)(p2 - 1) \cdots (pk - 1)
\]
Điều này là rất quan trọng để xác định khóa giải mã.

#### 3. Tính toán chỉ số riêng tư `d`
Chỉ số riêng tư `d` là nghịch đảo modular của `e` theo `φ(n)`:
\[
d = e^{-1} \pmod{φ(n)}
\]

#### 4. Giải mã dữ liệu
Sử dụng chỉ số riêng tư `d`, ta có thể giải mã dữ liệu `ct`:
\[
m = ct^d \bmod n
\]
Trong đó `m` là thông điệp đã giải mã.

#### 5. Chuyển đổi thông điệp sang định dạng có thể đọc được
Thông điệp `m` là một số, chúng ta có thể chuyển đổi số này thành chuỗi byte để lấy được flag.

### Giải pháp bằng Python
```python
from Crypto.Util.number import long_to_bytes

n = 580642391898843192929563856870897799650883152718761762932292482252152591279871421569162037190419036435041797739880389529593674485555792234900969402019055601781662044515999210032698275981631376651117318677368742867687180140048715627160641771118040372573575479330830092989800730105573700557717146251860588802509310534792310748898504394966263819959963273509119791037525504422606634640173277598774814099540555569257179715908642917355365791447508751401889724095964924513196281345665480688029639999472649549163147599540142367575413885729653166517595719991872223011969856259344396899748662101941230745601719730556631637
e = 65537
ct = 320721490534624434149993723527322977960556510750628354856260732098109692581338409999983376131354918370047625150454728718467998870322344980985635149656977787964380651868131740312053755501594999166365821315043312308622388016666802478485476059625888033017198083472976011719998333985531756978678758897472845358167730221506573817798467100023754709109274265835201757369829744113233607359526441007577850111228850004361838028842815813724076511058179239339760639518034583306154826603816927757236549096339501503316601078891287408682099750164720032975016814187899399273719181407940397071512493967454225665490162619270814464


phi = 580642391898843191487404652150193463439642600155214610402815446275117822457602964108279991178253399797937961990567828910318944376020941874995912942457183778540787232677949141800666918857974957805860863128934894322453334083108951829885566055541321469492863749601696156719452204625091396670183612468234453545730714411260422415053794985900973204357184470104831581957188055965458235216412636167147716884241110058234315146752181551500634472836779298794303330378218517375396697137335380548442818167481491481087606998467945980408909917714107491743183639877866494931448463312524563384587536906823474872320000000000000000

d = pow(e, -1, phi)
m = pow(ct, d, n)

print(long_to_bytes(m))
```

<img width="535" height="175" alt="image" src="https://github.com/user-attachments/assets/c4b1d894-bbbd-4ad6-a657-1a36f25c8f17" />

Flag: `crypto{700_m4ny_5m4ll_f4c70r5}`


## **12. Salty**

### Given
Bài toán yêu cầu giải mã dữ liệu RSA với các tham số `n`, `e`, và `ct` trong đó `n` là tích của nhiều số nguyên tố nhỏ.

#### Tham số
- **n**: Một số nguyên lớn là tích của nhiều số nguyên tố.
- **e**: Mũ công khai (`e = 1`).
- **ct**: Dữ liệu mã hóa (ciphertext) cần giải mã.

### Goal
- Vì `e = 1`, quá trình mã hóa và giải mã không thay đổi dữ liệu, tức là `ct` chính là `pt` (plaintext).
- Do đó, `ct` chính là dữ liệu gốc, và không cần phải giải mã.

### Solution

#### 1. Phân tích `n`
- `n` là tích của hai số nguyên tố `p` và `q`, nhưng vì `e = 1`, việc phân tích này không quan trọng với bài toán này.

#### 2. Tính hàm Euler `φ(n)`
- Vì `e = 1`, chúng ta không cần phải tính hàm Euler `φ(n)` để giải quyết bài toán này.

#### 3. Tính toán chỉ số riêng tư `d`
- Chỉ số riêng tư `d` là nghịch đảo của `e` theo `φ(n)`, nhưng vì `e = 1`, chúng ta có `d = 1`, và không cần tính toán thêm.

#### 4. Giải mã
- Dữ liệu mã hóa (`ct`) chính là dữ liệu gốc (`pt`), vì vậy chúng ta không cần giải mã.

#### 5. Chuyển đổi `ct` thành định dạng có thể đọc được
- Chúng ta chỉ cần chuyển đổi `ct` (là `pt`) từ dạng số nguyên sang dạng byte để lấy được flag.

### Code tìm FLAG
```python
from Crypto.Util.number import long_to_bytes

ct = 44981230718212183604274785925793145442655465025264554046028251311164494127485
flag = long_to_bytes(ct)
print(flag)
```

<img width="495" height="151" alt="image" src="https://github.com/user-attachments/assets/2f64f143-27eb-4048-a370-2ee05bb63c33" />


<img width="1482" height="385" alt="image" src="https://github.com/user-attachments/assets/6f4d9816-8a41-4d8e-b84d-d7f7fcdd0c75" />


## **13. Modulus Inutilis**

### Given
- **Khóa công khai**: \( e = 3 \)
- **Ciphertext**: \( ct \)
- **Modulus**: \( n \)
- **Flag cần giải mã**: \( \text{FLAG} = b"crypto{???????????????????????????"} \)

#### Mô tả về mã hóa RSA:
Trong hệ thống RSA, ciphertext \( ct \) được tính từ plaintext \( pt \) theo công thức:
\[
ct = pt^e \mod n
\]
Do đó, để giải mã được thông điệp, chúng ta cần tính toán giá trị \( pt \) từ \( ct \).

### Goal
- Mục tiêu là giải mã ciphertext \( ct \) và khôi phục lại giá trị của flag \( pt \).

### Solution

#### Các bước thực hiện:

1. **Phân tích \( N \)**:
   - Chúng ta cần phân tích modulus \( n \) thành hai yếu tố nguyên tố \( p \) và \( q \) để tính \( phi(N) = (p-1)(q-1) \).

2. **Tính \( d \)**:
   - Tính \( d \), nghịch đảo của \( e \) modulo \( \phi(N) \), để có thể giải mã ciphertext bằng công thức RSA:
   \[
   pt = ct^d \mod n
   \]

3. **Giải mã ciphertext**:
   - Sau khi có \( d \), chúng ta sẽ giải mã ciphertext để tính giá trị của \( pad\_msg \).

4. **Khôi phục lại flag**:
   - Bằng cách sử dụng công thức padding \( text{{pad\_msg}} = a \times m + b \), ta khôi phục lại giá trị \( m \) (flag) từ giá trị \( pad\_msg \):
   \[
   m = frac{{text{{pad\_msg}} - b}}{a}
   \]

5. **Chuyển đổi số nguyên thành flag**:
   - Cuối cùng, sau khi khôi phục được giá trị \( m \), chúng ta sẽ chuyển đổi \( m \) thành chuỗi bytes và in ra flag.

#### Code tìm FLAG
```python
from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes
from sympy import factorint, cbrt

n = 17258212916191948536348548470938004244269544560039009244721959293554822498047075403658429865201816363311805874117705688359853941515579440852166618074161313773416434156467811969628473425365608002907061241714688204565170146117869742910273064909154666642642308154422770994836108669814632309362483307560217924183202838588431342622551598499747369771295105890359290073146330677383341121242366368309126850094371525078749496850520075015636716490087482193603562501577348571256210991732071282478547626856068209192987351212490642903450263288650415552403935705444809043563866466823492258216747445926536608548665086042098252335883
e = 3
ct = 243251053617903760309941844835411292373350655973075480264001352919865180151222189820473358411037759381328642957324889519192337152355302808400638052620580409813222660643570085177957

factors = factorint(n)
p = list(factors.keys())[0]
q = list(factors.keys())[1]

phi = (p - 1) * (q - 1)

d = inverse(e, phi)

pad_msg = pow(ct, d, n)

a, b = 123456, 654321  # Thay giá trị a, b thật vào đây
m = (pad_msg - b) // a

flag = long_to_bytes(m)
print(f"Flag: {flag.decode()}")
```
<img width="512" height="98" alt="image" src="https://github.com/user-attachments/assets/d493bc10-3f57-4a5e-a014-b10f51dbcd33" />


<img width="1523" height="364" alt="image" src="https://github.com/user-attachments/assets/82bc956c-c115-4b1f-8e4e-bafeeb1934c6" />


## **14. Everything is Big**

<img width="2176" height="434" alt="image" src="https://github.com/user-attachments/assets/5e4c4783-4b6a-47f8-a1b0-3933dbb41fc9" />

#### Given
* [cite_start]Một hệ thống mã hóa RSA với các tham số $N$, $e$, và ciphertext $c$ có kích thước rất lớn (khoảng 2048 bits)[cite: 8].
* [cite_start]File `Everything is Big.py` cho thấy số mũ công khai $e$ cũng rất lớn, gần tương đương với kích thước của $N$[cite: 8].
* [cite_start]Thông thường trong RSA, người ta chọn $e$ nhỏ (như 65537) để tối ưu tốc độ mã hóa, nhưng ở đây $e$ được chọn "massive" (khổng lồ)[cite: 8].

#### Goal
* Khai thác việc sử dụng số mũ công khai $e$ quá lớn để tìm ra số mũ bí mật $d$ và giải mã Flag.

### Solution

#### **Phân tích lỗ hổng**
Trong RSA, nếu số mũ công khai $e$ rất lớn và gần bằng $N$, điều đó thường có nghĩa là số mũ bí mật $d$ sẽ rất nhỏ. Theo **Định lý Wiener (Wiener's Attack)**, nếu số mũ bí mật $d$ thỏa mãn điều kiện:
$$d < \frac{1}{3} N^{1/4}$$
thì ta có thể tìm ra $d$ một cách hiệu quả thông qua việc tính toán các liên phân số (continued fractions) của tỷ số $\frac{e}{N}$. Các giá trị xấp xỉ (convergents) của $\frac{e}{N}$ sẽ chứa giá trị $\frac{k}{d}$, từ đó giúp ta khôi phục được $d$.

#### **Các bước thực hiện**
1.  [cite_start]**Tính liên phân số:** Tính toán dãy liên phân số cho giá trị $\frac{e}{N}$[cite: 8].
2.  **Tìm Convergents:** Với mỗi giá trị xấp xỉ $\frac{k}{d}$ trong dãy:
    * Giả định mẫu số chính là số mũ bí mật $d$.
    * Kiểm tra xem $d$ có hợp lệ không bằng cách thử giải mã một phần bản tin hoặc kiểm tra tính chất $a^{ed} \equiv a \pmod N$.
3.  [cite_start]**Giải mã:** Sau khi tìm được $d$ chính xác, thực hiện phép tính $m = c^d \pmod N$[cite: 8].
4.  [cite_start]**Lấy Flag:** Chuyển đổi số nguyên $m$ thu được sang định dạng bytes bằng hàm `long_to_bytes` để đọc nội dung Flag[cite: 8].
``` python 
from Crypto.Util.number import long_to_bytes

# Dữ liệu từ output.txt
N = 0xb8af3d3afb893a602de4afe2a29d7615075d1e570f8bad8ebbe9b5b9076594cf06b6e7b30905b6420e950043380ea746f0a14dae34469aa723e946e484a58bcd92d1039105871ffd63ffe64534b7d7f8d84b4a569723f7a833e6daf5e182d658655f739a4e37bd9f4a44aff6ca0255cda5313c3048f56eed5b21dc8d88bf5a8f8379eac83d8523e484fa6ae8dbcb239e65d3777829a6903d779cd2498b255fcf275e5f49471f35992435ee7cade98c8e82a8beb5ce1749349caa16759afc4e799edb12d299374d748a9e3c82e1cc983cdf9daec0a2739dadcc0982c1e7e492139cbff18c5d44529407edfd8e75743d2f51ce2b58573fea6fbd4fe25154b9964d
e = 0x9ab58dbc8049b574c361573955f08ea69f97ecf37400f9626d8f5ac55ca087165ce5e1f459ef6fa5f158cc8e75cb400a7473e89dd38922ead221b33bc33d6d716fb0e4e127b0fc18a197daf856a7062b49fba7a86e3a138956af04f481b7a7d481994aeebc2672e500f3f6d8c581268c2cfad4845158f79c2ef28f242f4fa8f6e573b8723a752d96169c9d885ada59cdeb6dbe932de86a019a7e8fc8aeb07748cfb272bd36d94fe83351252187c2e0bc58bb7a0a0af154b63397e6c68af4314601e29b07caed301b6831cf34caa579eb42a8c8bf69898d04b495174b5d7de0f20cf2b8fc55ed35c6ad157d3e7009f16d6b61786ee40583850e67af13e9d25be3
c = 0x3f984ff5244f1836ed69361f29905ca1ae6b3dcf249133c398d7762f5e277919174694293989144c9d25e940d2f66058b2289c75d1b8d0729f9a7c4564404a5fd4313675f85f31b47156068878e236c5635156b0fa21e24346c2041ae42423078577a1413f41375a4d49296ab17910ae214b45155c4570f95ca874ccae9fa80433a1ab453cbb28d780c2f1f4dc7071c93aff3924d76c5b4068a0371dff82531313f281a8acadaa2bd5078d3ddcefcb981f37ff9b8b14c7d9bf1accffe7857160982a2c7d9ee01d3e82265eec9c7401ecc7f02581fd0d912684f42d1b71df87a1ca51515aab4e58fab4da96e154ea6cdfb573a71d81b2ea4a080a1066e1bc3474

def wiener_attack(e, n):
    # Triển khai thuật toán liên phân số để tìm d
    def continued_fraction(n, d):
        while d:
            yield n // d
            n, d = d, n % d

    def convergents(cf):
        n0, d0 = 0, 1
        n1, d1 = 1, 0
        for q in cf:
            n2, d2 = q * n1 + n0, q * d1 + d0
            yield n2, d2
            n0, d0, n1, d1 = n1, d1, n2, d2

    for k, d in convergents(continued_fraction(e, n)):
        if k == 0: continue
        if (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            # Kiểm tra xem phi có hợp lệ không (giải phương trình bậc 2 tìm p, q)
            # Hoặc đơn giản là thử giải mã c
            m = pow(c, d, n)
            flag = long_to_bytes(m)
            if b'crypto' in flag:
                return flag

print(wiener_attack(e, N))

```


`crypto{s0m3th1ng5_c4n_b3_t00_b1g}`


## **15. Crossed Wires**
### Given
* Một file `source.py` mô tả quy trình mã hóa: Flag được mã hóa liên tiếp qua nhiều người bạn, mỗi người sử dụng một số mũ công khai $e_i$ khác nhau nhưng dùng chung một Modulus $N$.
* File `output.txt` cung cấp:
    * Modulus $N$.
    * Một cặp $(e, d)$ đóng vai trò là "chìa khóa" phụ.
    * Danh sách các số mũ công khai của bạn bè: `friend_es = [106979, 108533, 69557, 97117, 103231]`.
    * Bản mã cuối cùng `cipher`.

### Goal
* Khôi phục lại Flag ban đầu từ bản mã đã bị mã hóa chồng chéo qua nhiều lớp số mũ.

### Solution

#### **Phân tích lỗ hổng**
1.  **Tính chất mã hóa RSA liên tiếp:** Khi một bản tin $m$ được mã hóa liên tiếp qua các số mũ $e_1, e_2, ..., e_n$ với cùng một $N$, bản mã cuối cùng sẽ là:
    $$C = m^{e_1 \cdot e_2 \cdot ... \cdot e_n} \pmod N$$
    Để giải mã, ta cần tìm số mũ giải mã tổng hợp $D$ sao cho $D \equiv (e_1 \cdot e_2 \cdot ... \cdot e_n)^{-1} \pmod{\phi(N)}$.
2.  **Khôi phục $\phi(N)$:** Ta không có $p, q$ để tính $\phi(N)$, nhưng đề bài cho một cặp $(e, d)$ hợp lệ. Theo lý thuyết RSA, nếu biết $N, e, d$, ta có thể phân tích thừa số $N$ thành $p$ và $q$ bằng thuật toán xác suất dựa trên việc tìm căn bậc hai của 1 modulo $N$.

#### **Các bước thực hiện**
1.  [cite_start]**Phân tích $N$:** Sử dụng cặp $(e, d)$ đã cho để tìm lại hai số nguyên tố $p$ và $q$. [cite: 1]
2.  [cite_start]**Tính toán $\phi(N)$:** Sau khi có $p$ và $q$, tính $\phi(N) = (p-1)(q-1)$. [cite: 1]
3.  **Tính số mũ mã hóa tổng hợp:** Nhân tất cả các số mũ trong `friend_es` lại với nhau theo modulo $\phi(N)$:
    $$E_{total} = \prod (friend\_es) \pmod{\phi(N)}$$
4.  [cite_start]**Tìm số mũ giải mã:** Tính số nghịch đảo modulo: $D_{total} = E_{total}^{-1} \pmod{\phi(N)}$. [cite: 1]
5.  [cite_start]**Giải mã:** Tính $Flag = cipher^{D_{total}} \pmod N$ và chuyển đổi kết quả từ số nguyên sang dạng bytes. [cite: 1]

---
``` python 
from Crypto.Util.number import long_to_bytes, inverse
import math
import random

# Dữ liệu từ output.txt 
N = 21711308225346315542706844618441565741046498277716979943478360598053144971379956916575370343448988601905854572029635846626259487297950305231661109855854947494209135205589258643517961521594924368498672064293208230802441077390193682958095111922082677813175804775628884377724377647428385841831277059274172982280545237765559969228707506857561215268491024097063920337721783673060530181637161577401589126558556182546896783307370517275046522704047385786111489447064794210010802761708615907245523492585896286374996088089317826162798278528296206977900274431829829206103227171839270887476436899494428371323874689055690729986771
d = 2734411677251148030723138005716109733838866545375527602018255159319631026653190783670493107936401603981429171880504360560494771017246468702902647370954220312452541342858747590576273775107870450853533717116684326976263006435733382045807971890762018747729574021057430331778033982359184838159747331236538501849965329264774927607570410347019418407451937875684373454982306923178403161216817237890962651214718831954215200637651103907209347900857824722653217179548148145687181377220544864521808230122730967452981435355334932104265488075777638608041325256776275200067541533022527964743478554948792578057708522350812154888097
e = 65537
cipher = 20304610279578186738172766224224793119885071262464464448863461184092225736054747976985179673905441502689126216282897704508745403799054734121583968853999791604281615154100736259131453424385364324630229671185343778172807262640709301838274824603101692485662726226902121105591137437331463201881264245562214012160875177167442010952439360623396658974413900469093836794752270399520074596329058725874834082188697377597949405779039139194196065364426213208345461407030771089787529200057105746584493554722790592530472869581310117300343461207750821737840042745530876391793484035024644475535353227851321505537398888106855012746117
friend_es = [106979, 108533, 69557, 97117, 103231] # 

# Bước 1: Phân tích N thành p, q dựa trên e, d
def get_factors(n, e, d):
    k = e * d - 1
    g = random.randint(2, n - 1)
    t = k
    while t % 2 == 0:
        t //= 2
        x = pow(g, t, n)
        if x > 1:
            y = math.gcd(x - 1, n)
            if y > 1:
                return y, n // y
    return None

p, q = get_factors(N, e, d)
phi = (p - 1) * (q - 1)

# Bước 2: Tính số mũ mã hóa tổng hợp (Product of all friends' e)
total_e = 1
for fe in friend_es:
    total_e = (total_e * fe) % phi

# Bước 3: Giải mã
total_d = inverse(total_e, phi)
flag_int = pow(cipher, total_d, N)

print(f"Flag: {long_to_bytes(flag_int).decode()}")

```
`crypto{3ncrypt_y0ur_s3cr3t_w1th_y0ur_fr1end5_publ1c_k3y}`

<img width="976" height="96" alt="image" src="https://github.com/user-attachments/assets/7a347808-88b7-4f89-8f4e-df1b56d3419d" />


## **16. Everything is Still Big**
### Given
Một hệ thống mã hóa RSA với Modulus $N$, số mũ công khai $e$ và Ciphertext $ct$ đều là các số cực kỳ lớn (2048-bit)[cite: 11].
Tên bài toán ám chỉ đây là phiên bản nâng cấp của "Everything is Big". [cite_start]Tuy nhiên, các giá trị $e$ và $d$ (số mũ bí mật) đã được điều chỉnh để tránh cuộc tấn công Wiener cơ bản[cite: 11].

### Goal
Khai thác cấu trúc của các số mũ RSA khi chúng quá lớn để tìm ra số mũ bí mật $d$ và giải mã Flag.

### Solution

#### **Phân tích lỗ hổng**
Mặc dù $e$ rất lớn, nhưng thử thách này vẫn đánh vào điểm yếu của việc chọn số mũ không an toàn. [cite_start]Khi $e$ có độ lớn xấp xỉ $N$, có khả năng cao là $d$ vẫn đủ nhỏ để bị tấn công bởi **Boneh-Durfee Attack**[cite: 11]. 
**Wiener's Attack** hoạt động khi $d < \frac{1}{3}N^{0.25}$.
**Boneh-Durfee Attack** là một bản nâng cấp sử dụng phương pháp Coppersmith (tìm nghiệm nhỏ của đa thức đa biến) để phá vỡ RSA khi $d < N^{0.292}$[cite: 11].

#### **Các bước thực hiện**
1.  [cite_start]**Xác định dạng tấn công:** Kiểm tra giá trị $e$ và $N$ từ file dữ liệu[cite: 11]. Nhận thấy $e$ rất lớn, ta áp dụng Boneh-Durfee Attack.
2.  **Thiết lập đa thức:** Xây dựng đa thức $f(x, y) = x(A + y) - 1 \equiv 0 \pmod e$, trong đó $x$ liên quan đến $d$ và $y$ liên quan đến $(p+q)$.
3.  [cite_start]**Sử dụng Lattice Reduction (LLL):** Tìm nghiệm nhỏ của đa thức trên bằng cách sử dụng thuật toán LLL (thường thực hiện trong môi trường `SageMath`)[cite: 11].
4.  **Khôi phục $d$:** Từ nghiệm của đa thức, ta tính toán ngược lại để tìm ra số mũ bí mật $d$.
5.  [cite_start]**Giải mã:** * Tính $m = ct^d \pmod N$[cite: 11].
    * [cite_start]Chuyển đổi kết quả $m$ từ số nguyên sang bytes bằng hàm `long_to_bytes()` để thu được Flag[cite: 11].


``` python 
import math

# Hàm hỗ trợ chuyển đổi số nguyên thành bytes nếu bạn chưa cài thư viện Crypto
def long_to_bytes(n):
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

# Dữ liệu đầy đủ từ file output_f554de954a6cd0a94142afc264107558.txt
N = 0xb12746657c720a434861e9a4828b3c89a6b8d4a1bd921054e48d47124dbcc9cfcdcc39261c5e93817c167db818081613f57729e0039875c72a5ae1f0bc5ef7c933880c2ad528adbc9b1430003a491e460917b34c4590977df47772fab1ee0ab251f94065ab3004893fe1b2958008848b0124f22c4e75f60ed3889fb62e5ef4dcc247a3d6e23072641e62566cd96ee8114b227b8f498f9a578fc6f687d07acdbb523b6029c5bbeecd5efaf4c4d35304e5e6b5b95db0e89299529eb953f52ca3247d4cd03a15939e7d638b168fd00a1cb5b0cc5c2cc98175c1ad0b959c2ab2f17f917c0ccee8c3fe589b4cb441e817f75e575fc96a4fe7bfea897f57692b050d2b
e = 0x9d0637faa46281b533e83cc37e1cf5626bd33f712cc1948622f10ec26f766fb37b9cd6c7a6e4b2c03bce0dd70d5a3a28b6b0c941d8792bc6a870568790ebcd30f40277af59e0fd3141e272c48f8e33592965997c7d93006c27bf3a2b8fb71831dfa939c0ba2c7569dd1b660efc6c8966e674fbe6e051811d92a802c789d895f356ceec9722d5a7b617d21b8aa42dd6a45de721953939a5a81b8dffc9490acd4f60b0c0475883ff7e2ab50b39b2deeedaefefffc52ae2e03f72756d9b4f7b6bd85b1a6764b31312bc375a2298b78b0263d492205d2a5aa7a227abaf41ab4ea8ce0e75728a5177fe90ace36fdc5dba53317bbf90e60a6f2311bb333bf55ba3245f
c = 0xa3bce6e2e677d7855a1a7819eb1879779d1e1eefa21a1a6e205c8b46fdc020a2487fdd07dbae99274204fadda2ba69af73627bdddcb2c403118f507bca03cb0bad7a8cd03f70defc31fa904d71230aab98a10e155bf207da1b1cac1503f48cab3758024cc6e62afe99767e9e4c151b75f60d8f7989c152fdf4ff4b95ceed9a7065f38c68dee4dd0da503650d3246d463f504b36e1d6fafabb35d2390ecf0419b2bb67c4c647fb38511b34eb494d9289c872203fa70f4084d2fa2367a63a8881b74cc38730ad7584328de6a7d92e4ca18098a15119baee91237cea24975bdfc19bdbce7c1559899a88125935584cd37c8dd31f3f2b4517eefae84e7e588344fa5

# Số d đã được tìm thấy qua thuật toán Wiener's attack
d = 4405001203086303853525638270840706181413309101774712363141310824943602913458674670435988275467396881342752245170076677567586495166847569659096584522419007

# Giải mã và in kết quả
m = pow(c, d, N)
print(f"Flag: {long_to_bytes(m).decode()}")
```
`crypto{bon3h5_4tt4ck_i5_sr0ng3r_th4n_w13n3r5}`


## **17. Endless Emails**
### Given
* Một danh sách nhiều cặp Modulus $n_i$ và Ciphertext $c_i$ tương ứng.
* Tất cả các tin nhắn đều sử dụng cùng một số mũ công khai nhỏ: $e = 3$.
* Bản rõ $m$ (Flag) được mã hóa nhiều lần với các khóa công khai khác nhau.

### Goal
* Khôi phục lại bản rõ $m$ khi biết cùng một nội dung được mã hóa với nhiều Modulus khác nhau nhưng dùng chung một số mũ $e$ nhỏ.

### Solution

#### **Phân tích lỗ hổng**
Đây là kịch bản điển hình của **Håstad's Broadcast Attack**. 
* Trong RSA, nếu cùng một thông điệp $m$ được gửi cho $k$ người dùng với cùng số mũ $e$, và $k \ge e$, ta có thể sử dụng **Định lý số dư Trung Hoa (Chinese Remainder Theorem - CRT)** để giải bài toán.
* Ở đây $e = 3$, và chúng ta có nhiều hơn 3 cặp $(n, c)$, thỏa mãn điều kiện để tấn công.

#### **Các bước thực hiện**
1.  **Hệ phương trình đồng dư:** Ta có hệ:
    * $m^3 \equiv c_1 \pmod{n_1}$
    * $m^3 \equiv c_2 \pmod{n_2}$
    * $m^3 \equiv c_3 \pmod{n_3}$
2.  **Áp dụng CRT:** Tìm một giá trị $C$ duy nhất sao cho $C \equiv m^3 \pmod{n_1 \cdot n_2 \cdot n_3}$.
3.  **Khai căn bậc $e$:** Vì $m < n_i$ nên $m^3 < n_1 \cdot n_2 \cdot n_3$. Điều này có nghĩa là giá trị $C$ tìm được chính là $m^3$ trên tập số nguyên (không còn là phép đồng dư modulo nữa).
4.  **Kết quả:** Tính căn bậc 3 của $C$ để tìm ra số nguyên $m$, sau đó chuyển đổi sang bytes để lấy Flag.

``` python 
from Crypto.Util.number import*
from itertools import *
import gmpy2
n = [14528915758150659907677315938876872514853653132820394367681510019000469589767908107293777996420037715293478868775354645306536953789897501630398061779084810058931494642860729799059325051840331449914529594113593835549493208246333437945551639983056810855435396444978249093419290651847764073607607794045076386643023306458718171574989185213684263628336385268818202054811378810216623440644076846464902798568705083282619513191855087399010760232112434412274701034094429954231366422968991322244343038458681255035356984900384509158858007713047428143658924970374944616430311056440919114824023838380098825914755712289724493770021, 20463913454649855046677206889944639231694511458416906994298079596685813354570085475890888433776403011296145408951323816323011550738170573801417972453504044678801608709931200059967157605416809387753258251914788761202456830940944486915292626560515250805017229876565916349963923702612584484875113691057716315466239062005206014542088484387389725058070917118549621598629964819596412564094627030747720659155558690124005400257685883230881015636066183743516494701900125788836869358634031031172536767950943858472257519195392986989232477630794600444813136409000056443035171453870906346401936687214432176829528484662373633624123, 19402640770593345339726386104915705450969517850985511418263141255686982818547710008822417349818201858549321868878490314025136645036980129976820137486252202687238348587398336652955435182090722844668488842986318211649569593089444781595159045372322540131250208258093613844753021272389255069398553523848975530563989367082896404719544411946864594527708058887475595056033713361893808330341623804367785721774271084389159493974946320359512776328984487126583015777989991635428744050868653379191842998345721260216953918203248167079072442948732000084754225272238189439501737066178901505257566388862947536332343196537495085729147, 12005639978012754274325188681720834222130605634919280945697102906256738419912110187245315232437501890545637047506165123606573171374281507075652554737014979927883759915891863646221205835211640845714836927373844277878562666545230876640830141637371729405545509920889968046268135809999117856968692236742804637929866632908329522087977077849045608566911654234541526643235586433065170392920102840518192803854740398478305598092197183671292154743153130012885747243219372709669879863098708318993844005566984491622761795349455404952285937152423145150066181043576492305166964448141091092142224906843816547235826717179687198833961, 17795451956221451086587651307408104001363221003775928432650752466563818944480119932209305765249625841644339021308118433529490162294175590972336954199870002456682453215153111182451526643055812311071588382409549045943806869173323058059908678022558101041630272658592291327387549001621625757585079662873501990182250368909302040015518454068699267914137675644695523752851229148887052774845777699287718342916530122031495267122700912518207571821367123013164125109174399486158717604851125244356586369921144640969262427220828940652994276084225196272504355264547588369516271460361233556643313911651916709471353368924621122725823, 25252721057733555082592677470459355315816761410478159901637469821096129654501579313856822193168570733800370301193041607236223065376987811309968760580864569059669890823406084313841678888031103461972888346942160731039637326224716901940943571445217827960353637825523862324133203094843228068077462983941899571736153227764822122334838436875488289162659100652956252427378476004164698656662333892963348126931771536472674447932268282205545229907715893139346941832367885319597198474180888087658441880346681594927881517150425610145518942545293750127300041942766820911120196262215703079164895767115681864075574707999253396530263, 19833203629283018227011925157509157967003736370320129764863076831617271290326613531892600790037451229326924414757856123643351635022817441101879725227161178559229328259469472961665857650693413215087493448372860837806619850188734619829580286541292997729705909899738951228555834773273676515143550091710004139734080727392121405772911510746025807070635102249154615454505080376920778703360178295901552323611120184737429513669167641846902598281621408629883487079110172218735807477275590367110861255756289520114719860000347219161944020067099398239199863252349401303744451903546571864062825485984573414652422054433066179558897]
c = [6965891612987861726975066977377253961837139691220763821370036576350605576485706330714192837336331493653283305241193883593410988132245791554283874785871849223291134571366093850082919285063130119121338290718389659761443563666214229749009468327825320914097376664888912663806925746474243439550004354390822079954583102082178617110721589392875875474288168921403550415531707419931040583019529612270482482718035497554779733578411057633524971870399893851589345476307695799567919550426417015815455141863703835142223300228230547255523815097431420381177861163863791690147876158039619438793849367921927840731088518955045807722225, 5109363605089618816120178319361171115590171352048506021650539639521356666986308721062843132905170261025772850941702085683855336653472949146012700116070022531926476625467538166881085235022484711752960666438445574269179358850309578627747024264968893862296953506803423930414569834210215223172069261612934281834174103316403670168299182121939323001232617718327977313659290755318972603958579000300780685344728301503641583806648227416781898538367971983562236770576174308965929275267929379934367736694110684569576575266348020800723535121638175505282145714117112442582416208209171027273743686645470434557028336357172288865172, 5603386396458228314230975500760833991383866638504216400766044200173576179323437058101562931430558738148852367292802918725271632845889728711316688681080762762324367273332764959495900563756768440309595248691744845766607436966468714038018108912467618638117493367675937079141350328486149333053000366933205635396038539236203203489974033629281145427277222568989469994178084357460160310598260365030056631222346691527861696116334946201074529417984624304973747653407317290664224507485684421999527164122395674469650155851869651072847303136621932989550786722041915603539800197077294166881952724017065404825258494318993054344153, 1522280741383024774933280198410525846833410931417064479278161088248621390305797210285777845359812715909342595804742710152832168365433905718629465545306028275498667935929180318276445229415104842407145880223983428713335709038026249381363564625791656631137936935477777236936508600353416079028339774876425198789629900265348122040413865209592074731028757972968635601695468594123523892918747882221891834598896483393711851510479989203644477972694520237262271530260496342247355761992646827057846109181410462131875377404309983072358313960427035348425800940661373272947647516867525052504539561289941374722179778872627956360577, 8752507806125480063647081749506966428026005464325535765874589376572431101816084498482064083887400646438977437273700004934257274516197148448425455243811009944321764771392044345410680448204581679548854193081394891841223548418812679441816502910830861271884276608891963388657558218620911858230760629700918375750796354647493524576614017731938584618983084762612414591830024113057983483156974095503392359946722756364412399187910604029583464521617256125933111786441852765229820406911991809039519015434793656710199153380699319611499255869045311421603167606551250174746275803467549814529124250122560661739949229005127507540805, 23399624135645767243362438536844425089018405258626828336566973656156553220156563508607371562416462491581383453279478716239823054532476006642583363934314982675152824147243749715830794488268846671670287617324522740126594148159945137948643597981681529145611463534109482209520448640622103718682323158039797577387254265854218727476928164074249568031493984825273382959147078839665114417896463735635546290504843957780546550577300001452747760982468547756427137284830133305010038339400230477403836856663883956463830571934657200851598986174177386323915542033293658596818231793744261192870485152396793393026198817787033127061749, 15239683995712538665992887055453717247160229941400011601942125542239446512492703769284448009141905335544729440961349343533346436084176947090230267995060908954209742736573986319254695570265339469489948102562072983996668361864286444602534666284339466797477805372109723178841788198177337648499899079471221924276590042183382182326518312979109378616306364363630519677884849945606288881683625944365927809405420540525867173639222696027472336981838588256771671910217553150588878434061862840893045763456457939944572192848992333115479951110622066173007227047527992906364658618631373790704267650950755276227747600169403361509144]
e= 3
for i, j, k in combinations(range(7), 3):
    N=n[i]*n[j]*n[k]
    N1=N//n[i]
    N2=N//n[j]
    N3=N//n[k]
    u1 = inverse(N1, n[i]) 
    u2 = inverse(N2, n[j])
    u3 = inverse(N3, n[k])
    M = (c[i]*u1*N1 + c[k]*u3*N3 + c[j]*u2*N2) % N
    m = long_to_bytes(gmpy2.iroot(M, e)[0])
    if b'crypto{' in m:
        print(m.decode()) 
```
`crypto{1f_y0u_d0nt_p4d_y0u_4r3_Vuln3rabl3}`


## **18. Infinite Descent**
### Given
* Một file `descent.py` mô tả cách sinh các số nguyên tố $p$ và $q$ cho hệ thống RSA.
* Điểm đặc biệt: Để "tối ưu hóa" tốc độ, người tạo đã chọn $p$ và $q$ cực kỳ gần nhau (khoảng cách giữa chúng rất nhỏ).
* File `output.txt` cung cấp giá trị Modulus $N$, số mũ công khai $e = 65537$, và Ciphertext $ct$.

### Goal
* Phân tích Modulus $N$ thành $p$ và $q$ khi biết chúng nằm rất gần nhau trên trục số, từ đó giải mã Flag.

### Solution

#### **Phân tích lỗ hổng**
Đây là kịch bản hoàn hảo cho **Thuật toán phân tích thừa số của Fermat (Fermat's Factorization Method)**.
* Khi $p$ và $q$ gần nhau, giá trị trung bình $a = \frac{p+q}{2}$ sẽ rất gần với $\sqrt{N}$.
* Ta có thể biểu diễn $N = a^2 - b^2$, với $b = \frac{p-q}{2}$.
* Nếu $p \approx q$, thì $b$ là một số nhỏ. Khi đó $a^2 - N = b^2$ sẽ là một số chính phương. Ta chỉ cần kiểm tra các giá trị $a$ bắt đầu từ $\lceil\sqrt{N}\rceil$ cho đến khi tìm được $a^2 - N$ là số chính phương.

#### **Các bước thực hiện**
1.  **Tính căn bậc hai:** Đặt $a = \text{isqrt}(N) + 1$.
2.  **Vòng lặp Fermat:**
    * Tính $b^2 = a^2 - N$.
    * Kiểm tra nếu $b^2$ là một số chính phương (tức là $\lfloor\sqrt{b^2}\rfloor^2 = b^2$).
    * Nếu không phải, tăng $a$ lên 1 đơn vị và lặp lại.
3.  **Tìm $p, q$:** Khi tìm thấy số chính phương, tính $p = a + b$ và $q = a - b$.
4.  **Giải mã RSA:**
    * Tính $\phi(N) = (p-1)(q-1)$.
    * Tính $d = e^{-1} \pmod{\phi(N)}$.
    * Tính $m = ct^d \pmod N$ và dùng `long_to_bytes` để lấy Flag.
``` python 
import math
from Crypto.Util.number import long_to_bytes, inverse

def isqrt(n):
    """Hàm tính căn bậc hai số nguyên (Newton's method)"""
    if n < 0:
        raise ValueError("Không thể tính căn bậc hai của số âm")
    if n == 0:
        return 0
    x = 2**(n.bit_length() // 2 + 1)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y

def fermat(n):
    """Thuật toán phân tích thừa số Fermat"""
    if n % 2 == 0:
        return 2, n // 2

    a = isqrt(n)
    if a * a < n:
        a += 1
        
    b2 = a*a - n
    b = isqrt(b2)

    max_iterations = 1000000 # Tăng giới hạn lặp để an toàn
    count = 0

    while b*b != b2:
        a += 1
        b2 = a*a - n
        b = isqrt(b2)
        count += 1

        if count > max_iterations:
            raise Exception(f"Không thể phân tích sau {max_iterations} lần lặp")

    p = a + b
    q = a - b
    assert n == p * q
    return p, q

def main():
    # Giá trị n (Modulus)
    n = 383347712330877040452238619329524841763392526146840572232926924642094891453979246383798913394114305368360426867021623649667024217266529000859703542590316063318592391925062014229671423777796679798747131250552455356061834719512365575593221216339005132464338847195248627639623487124025890693416305788160905762011825079336880567461033322240015771102929696350161937950387427696385850443727777996483584464610046380722736790790188061964311222153985614287276995741553706506834906746892708903948496564047090014307484054609862129530262108669567834726352078060081889712109412073731026030466300060341737504223822014714056413752165841749368159510588178604096191956750941078391415634472219765129561622344109769892244712668402761549412177892054051266761597330660545704317210567759828757156904778495608968785747998059857467440128156068391746919684258227682866083662345263659558066864109212457286114506228470930775092735385388316268663664139056183180238043386636254075940621543717531670995823417070666005930452836389812129462051771646048498397195157405386923446893886593048680984896989809135802276892911038588008701926729269812453226891776546037663583893625479252643042517196958990266376741676514631089466493864064316127648074609662749196545969926051
    
    # Phân tích n thành p và q
    print("[*] Đang phân tích n bằng thuật toán Fermat...")
    p, q = fermat(n)
    print(f"[+] Tìm thấy p: {p}")
    print(f"[+] Tìm thấy q: {q}")
    
    # Giá trị Ciphertext và e
    c = 98280456757136766244944891987028935843441533415613592591358482906016439563076150526116369842213103333480506705993633901994107281890187248495507270868621384652207697607019899166492132408348789252555196428608661320671877412710489782358282011364127799563335562917707783563681920786994453004763755404510541574502176243896756839917991848428091594919111448023948527766368304503100650379914153058191140072528095898576018893829830104362124927140555107994114143042266758709328068902664037870075742542194318059191313468675939426810988239079424823495317464035252325521917592045198152643533223015952702649249494753395100973534541766285551891859649320371178562200252228779395393974169736998523394598517174182142007480526603025578004665936854657294541338697513521007818552254811797566860763442604365744596444735991732790926343720102293453429936734206246109968817158815749927063561835274636195149702317415680401987150336994583752062565237605953153790371155918439941193401473271753038180560129784192800351649724465553733201451581525173536731674524145027931923204961274369826379325051601238308635192540223484055096203293400419816024111797903442864181965959247745006822690967920957905188441550106930799896292835287867403979631824085790047851383294389
    e = 65537
    
    # Tính số mũ giải mã d
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    
    # Giải mã thông điệp m = c^d mod n
    m = pow(c, d, n)
    
    # Chuyển số sang chuỗi bytes (Flag)
    flag = long_to_bytes(m)
    print(f"\n[+] Flag tìm được: {flag.decode()}")

if __name__ == '__main__':
    main()
```
<img width="720" height="102" alt="image" src="https://github.com/user-attachments/assets/1d1a40b8-5e08-44da-a326-7f007c666b0a" />


`crypto{f3rm47_w45_4_g3n1u5}`



## **19.Marin's Secrets**
### Given
* File `marin.py` mô tả cách sinh hai số nguyên tố $p$ và $q$ từ một danh sách bí mật.
* Hàm `get_prime(secret)` thực hiện phép tính: `(1 << secret) - 1`. Đây chính là công thức của **Số nguyên tố Mersenne**: $M_n = 2^n - 1$.
* File `output.txt` cung cấp:
    * Modulus $n$ (tích của hai số nguyên tố Mersenne).
    * Số mũ công khai $e = 65537$.
    * Ciphertext $c$.

### Goal
* Phân tích $n$ thành hai thừa số $p$ và $q$. Vì $p, q$ có dạng đặc biệt $2^x - 1$, việc tìm ra chúng dễ dàng hơn nhiều so với phân tích số nguyên thông thường.

### Solution

#### **Phân tích lỗ hổng**
Tên thử thách "Marin" ám chỉ nhà toán học **Marin Mersenne**. Các số nguyên tố Mersenne rất hiếm và đã được lập danh sách cụ thể. 

Thay vì dùng các thuật toán phân tích thừa số vạn năng như GNFS, ta chỉ cần thử chia $n$ cho các số trong danh sách số nguyên tố Mersenne đã biết. Nếu $n$ chia hết cho một số $M_p$, ta tìm được thừa số thứ nhất, từ đó suy ra thừa số còn lại.

#### **Các bước thực hiện**
1.  **Liệt kê số Mersenne:** Sử dụng danh sách các số mũ $s$ sao cho $2^s - 1$ là số nguyên tố (ví dụ: 2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281...).
2.  **Tìm $p$ và $q$:** * Thử lần lượt các số $p = 2^s - 1$.
    * Kiểm tra nếu $n \pmod p == 0$. 
    * Trong bài này, qua tính toán ta tìm được $p = 2^{2203} - 1$ và $q = 2^{2281} - 1$.
3.  **Giải mã RSA:**
    * Tính $\phi(n) = (p-1)(q-1)$.
    * Tính số mũ giải mã $d = e^{-1} \pmod{\phi(n)}$.
    * Tính bản rõ $m = c^d \pmod n$.
4.  **Lấy Flag:** Chuyển số nguyên $m$ sang định dạng bytes để thu được chuỗi flag.


`crypto{Th3se_Pr1m3s_4r3_t00_r4r3}`
<img width="2068" height="78" alt="image" src="https://github.com/user-attachments/assets/16aa7525-dcba-4ab1-9932-44b70df62461" />


## **20. Fast Primes**
### Given
* Một hệ thống sinh khóa RSA được quảng cáo là "siêu nhanh" so với cách truyền thống.
* File `key.pem` chứa khóa công khai (Public Key).
* File `ciphertext.txt` chứa bản mã của flag, được mã hóa bằng chuẩn **PKCS1_OAEP**.
* Bản chất của "Fast Primes" thường nằm ở việc sử dụng một bộ sinh số ngẫu nhiên (PRNG) yếu hoặc các số nguyên tố được sinh ra có cấu trúc đặc biệt để giảm thời gian kiểm tra tính nguyên tố.

### Goal
* Phân tích số Modulus $N$ từ khóa công khai để tìm ra hai thừa số nguyên tố $p$ và $q$, từ đó tính toán số mũ bí mật $d$ và giải mã flag.

### Solution

#### **Phân tích lỗ hổng**
Trong các bài tập RSA "Fast Primes" (hoặc các lỗ hổng thực tế như ROCA), lỗ hổng thường nằm ở cách chọn $p$ và $q$. 
* Nếu $p$ và $q$ được sinh ra quá nhanh bằng cách kết hợp các số nguyên tố nhỏ hoặc sử dụng một hàm toán học thiếu tính ngẫu nhiên, Modulus $N$ sẽ dễ dàng bị phân tích bởi các trang web như **factordb.com** hoặc các thuật toán phân tích thừa số như **Pollard's rho**, **ECM**.
* Trong trường hợp này, $N$ đã được cộng đồng giải mã trước đó và kết quả phân tích có sẵn trên cơ sở dữ liệu trực tuyến.

#### **Các bước thực hiện**
1.  **Trích xuất Public Key:** Sử dụng thư viện `Crypto.PublicKey.RSA` để đọc file `key.pem` và lấy giá trị Modulus $N$ cùng số mũ $e$.
2.  **Phân tích $N$ thành $p, q$:** * Cách nhanh nhất là đưa giá trị $N$ lên [factordb.com](http://factordb.com). 
    * Kết quả trả về sẽ là hai số nguyên tố $p$ và $q$.
3.  **Khôi phục Private Key:** * Tính $\phi(N) = (p-1)(q-1)$.
    * Tính số mũ bí mật $d = e^{-1} \pmod{\phi(N)}$.
    * Tạo lại đối tượng khóa RSA đầy đủ bằng bộ $(N, e, d, p, q)$.
4.  **Giải mã Flag:** * Sử dụng thư viện `Crypto.Cipher.PKCS1_OAEP` kết hợp với Private Key vừa khôi phục.
    * Giải mã nội dung từ file `ciphertext.txt` để lấy Flag.
``` python 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import inverse

# 1. Thông số đã cho
p = 51894141255108267693828471848483688186015845988173648228318286999011443419469
q = 77342270837753916396402614215980760127245056504361515489809293852222206596161
n = p * q
e = 65537 # Thông thường e là 65537, nếu key.pem của bạn khác hãy sửa lại

# 2. Tính toán các thông số RSA
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

# 3. Khởi tạo Key RSA
# Sử dụng bộ (n, e, d, p, q) giúp thư viện xử lý nhanh và chính xác hơn
key_params = (n, e, d, p, q)
key = RSA.construct(key_params)

# 4. Dữ liệu bản mã (Ciphertext)
c_hex = "249d72cd1d287b1a15a3881f2bff5788bc4bf62c789f2df44d88aae805b54c9a94b8944c0ba798f70062b66160fee312b98879f1dd5d17b33095feb3c5830d28"
ciphertext = bytes.fromhex(c_hex)

# 5. Giải mã sử dụng PKCS1_OAEP
try:
    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(ciphertext)
    print("Nội dung giải mã (Flag):")
    print(plaintext.decode())
except ValueError as e:
    print(f"Lỗi giải mã: {e}")
    print("Có thể bản mã hoặc các số nguyên tố p, q không khớp với khóa.")
```
<img width="1300" height="108" alt="image" src="https://github.com/user-attachments/assets/7011adcc-8028-409c-aa01-b292289f81c2" />

`crypto{p00R_3570n14}s`



## **21. Ron was Wrong, Whit is Right**
### Given
* **Dữ liệu:** Một file zip chứa 50 cặp file (khóa công khai `.pem` và bản mã `.ciphertext`).
* **Giao thức:** Sử dụng RSA với chuẩn mã hóa PKCS#1 OAEP.
* **Tên bài toán:** "Ron" (Rivest) và "Whit" (Diffie) ám chỉ các nhà sáng lập RSA và Diffie-Hellman. Lỗi này thường liên quan đến cách sinh số ngẫu nhiên kém dẫn đến trùng lặp.

### Goal
* Phân tích 50 Modulus $N_i$ để tìm xem có cặp nào dùng chung số nguyên tố hay không. Nếu có, ta có thể phân tích thừa số $N$ ngay lập tức.

### Solution

#### **Lỗ hổng Batch GCD**
Nếu hai Modulus $N_1 = p \cdot q_1$ và $N_2 = p \cdot q_2$ dùng chung một số nguyên tố $p$, ta có thể tìm ra $p$ cực nhanh bằng cách tính:
$$p = \text{gcd}(N_1, N_2)$$
Sau khi có $p$, ta tìm được $q_1 = N_1 / p$ và $q_2 = N_2 / p$. Từ đó tính được số mũ giải mã $d$ cho cả hai khóa.



#### **Các bước thực hiện (Dựa trên code giải của bạn)**
1. **Thu thập:** Đọc tất cả 50 file `.pem` để lấy danh sách các số $N_i$ và $e_i$.
2. **So sánh cặp:** Duyệt qua tất cả các cặp $(N_i, N_j)$. Với mỗi cặp, tính `gcd(Ni, Nj)`.
3. **Kiểm tra:** Nếu kết quả $gcd > 1$, ta đã tìm thấy số nguyên tố dùng chung $p$.
4. **Giải mã:**
   * Tính $q = N_i / p$.
   * Tính $\phi(N_i) = (p-1)(q-1)$.
   * Tính $d = e_i^{-1} \pmod{\phi(N_i)}$.
   * Sử dụng thư viện `Crypto.Cipher.PKCS1_OAEP` để giải mã file `.ciphertext` tương ứng.

### **4. Kết quả**
Khi chạy script, bạn sẽ tìm thấy một vài cặp khóa bị lỗi "vòng lặp sinh số ngẫu nhiên" và dùng chung $p$. Giải mã các file này sẽ thu được Flag.

``` python
import os
from math import gcd
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Lấy đường dẫn thư mục hiện tại (nơi bạn đang đứng trong Terminal)
current_dir = os.getcwd() 

def solve():
    keys = []
    ciphertexts = {}

    print(f"[*] Đang tìm file tại: {current_dir}")

    # 1. Đọc dữ liệu
    for i in range(1, 51):
        pem_path = os.path.join(current_dir, f"{i}.pem")
        cit_path = os.path.join(current_dir, f"{i}.ciphertext")
        
        if os.path.exists(pem_path) and os.path.exists(cit_path):
            with open(pem_path, 'r') as f:
                key = RSA.import_key(f.read())
            with open(cit_path, 'r') as f:
                c_hex = f.read().strip()
            
            # Sửa lỗi in ấn ở đây: ép kiểu sang string trước khi cắt [:20]
            print(f"[+] Đã đọc: {i}.pem - Modulus: {str(key.n)[:20]}...")
            
            keys.append({'id': i, 'n': key.n, 'e': key.e})
            ciphertexts[i] = bytes.fromhex(c_hex)

    if not keys:
        print("[-] Vẫn không thấy file nào. Bạn có chắc file nằm trong thư mục 'Pemfile' không?")
        return

    # 2. Tấn công Batch GCD
    print(f"[*] Đang so sánh {len(keys)} khóa để tìm GCD...")
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            n1, n2 = keys[i]['n'], keys[j]['n']
            p = gcd(n1, n2)
            
            if 1 < p < n1:
                print(f"\n[!] BINGO! Tìm thấy ước chung p giữa file {keys[i]['id']} và {keys[j]['id']}")
                
                # Giải mã
                for target in [keys[i], keys[j]]:
                    n, e, idx = target['n'], target['e'], target['id']
                    q = n // p
                    phi = (p - 1) * (q - 1)
                    d = pow(e, -1, phi)
                    
                    priv_key = RSA.construct((n, e, d, p, q))
                    cipher = PKCS1_OAEP.new(priv_key)
                    
                    try:
                        flag = cipher.decrypt(ciphertexts[idx])
                        print(f"===> FLAG ({idx}): {flag.decode()}")
                    except:
                        continue
                return

if __name__ == "__main__":
    solve()
```
`crypto{3ucl1d_w0uld_b3_pr0ud}`



## **22. RSA Backdoor Viability**

### Given
Bài này cho file sinh khóa `complex_primes.py` và file `output.txt` chứa `n`, `e`, `c`.

Từ source code, ta có:

- `q` là một số nguyên tố 2048-bit bình thường.
- `p` không phải prime ngẫu nhiên chuẩn, mà được sinh bởi hàm:

```python
def get_complex_prime():
    D = 427
    while True:
        s = random.randint(2 ** 1020, 2 ** 1021 - 1)
        tmp = D * s ** 2 + 1
        if tmp % 4 == 0 and isPrime((tmp // 4)):
            return tmp // 4
```

Suy ra:

\[
p = frac{427s^2 + 1}{4}
\]

hay tương đương:

\[
4p - 1 = 427s^2
\]

Đây là một dạng prime đặc biệt, thuộc nhóm prime có thể bị factor bằng kỹ thuật **Complex Multiplication (CM)**, còn hay được gọi là hướng tấn công kiểu **4p - 1 factorization**.

---

### Ý tưởng giải

RSA bình thường an toàn vì rất khó factor:

\[
n = p cdot q
\]

Nhưng ở đây `p` được tạo theo một công thức đặc biệt:

\[
4p - 1 = 427s^2
\]

Nên `p` không còn là random prime “đẹp” nữa. Đây chính là “backdoor” mà đề bài nhắc tới.

Vì vậy hướng giải là:

1. Nhận ra `p` có cấu trúc đặc biệt từ source.
2. Dùng CM-based factorization / 4p-1 method để factor `n`.
3. Sau khi có `p`, `q`, tính:
   \[
   \varphi(n) = (p-1)(q-1)
   \]
4. Tính khóa bí mật:
   \[
   d = e^{-1} \bmod \varphi(n)
   \]
5. Giải mã:
   \[
   m = c^d \bmod n
   \]
6. Đổi `m` sang bytes để lấy flag.



### Sau khi factor `n`

Thu được:

```python
p = 20365029276121374486239093637518056591173153560816088704974934225137631026021006278728172263067093375127799517021642683026453941892085549596415559632837140072587743305574479218628388191587060262263170430315761890303990233871576860551166162110565575088243122411840875491614571931769789173216896527668318434571140231043841883246745997474500176671926153616168779152400306313362477888262997093036136582318881633235376026276416829652885223234411339116362732590314731391770942433625992710475394021675572575027445852371400736509772725581130537614203735350104770971283827769016324589620678432160581245381480093375303381611323

q = 34857423162121791604235470898471761566115159084585269586007822559458774716277164882510358869476293939176287610274899509786736824461740603618598549945273029479825290459062370424657446151623905653632181678065975472968242822859926902463043730644958467921837687772906975274812905594211460094944271575698004920372905721798856429806040099698831471709774099003441111568843449452407542799327467944685630258748028875103444760152587493543799185646692684032460858150960790495575921455423185709811342689185127936111993248778962219413451258545863084403721135633428491046474540472029592613134125767864006495572504245538373207974181
```

---

### Code giải

```python
from Crypto.Util.number import inverse, long_to_bytes

n = 709872443186761582125747585668724501268558458558798673014673483766300964836479167241315660053878650421761726639872089885502004902487471946410918420927682586362111137364814638033425428214041019139158018673749256694555341525164012369589067354955298579131735466795918522816127398340465761406719060284098094643289390016311668316687808837563589124091867773655044913003668590954899705366787080923717270827184222673706856184434629431186284270269532605221507485774898673802583974291853116198037970076073697225047098901414637433392658500670740996008799860530032515716031449787089371403485205810795880416920642186451022374989891611943906891139047764042051071647203057520104267427832746020858026150611650447823314079076243582616371718150121483335889885277291312834083234087660399534665835291621232056473843224515909023120834377664505788329527517932160909013410933312572810208043849529655209420055180680775718614088521014772491776654380478948591063486615023605584483338460667397264724871221133652955371027085804223956104532604113969119716485142424996255737376464834315527822566017923598626634438066724763559943441023574575168924010274261376863202598353430010875182947485101076308406061724505065886990350185188453776162319552566614214624361251463
e = 65537
c = 608484617316138126443275660524263025508135383745665175433229598517433030003704261658172582370543758277685547533834085899541036156595489206369279739210904154716464595657421948607569920498815631503197235702333017824993576326860166652845334617579798536442066184953550975487031721085105757667800838172225947001224495126390587950346822978519677673568121595427827980195332464747031577431925937314209391433407684845797171187006586455012364702160988147108989822392986966689057906884691499234298351003666019957528738094330389775054485731448274595330322976886875528525229337512909952391041280006426003300720547721072725168500104651961970292771382390647751450445892361311332074663895375544959193148114635476827855327421812307562742481487812965210406231507524830889375419045542057858679609265389869332331811218601440373121797461318931976890674336807528107115423915152709265237590358348348716543683900084640921475797266390455366908727400038393697480363793285799860812451995497444221674390372255599514578194487523882038234487872223540513004734039135243849551315065297737535112525440094171393039622992561519170849962891645196111307537341194621689797282496281302297026025131743423205544193536699103338587843100187637572006174858230467771942700918388

p = 20365029276121374486239093637518056591173153560816088704974934225137631026021006278728172263067093375127799517021642683026453941892085549596415559632837140072587743305574479218628388191587060262263170430315761890303990233871576860551166162110565575088243122411840875491614571931769789173216896527668318434571140231043841883246745997474500176671926153616168779152400306313362477888262997093036136582318881633235376026276416829652885223234411339116362732590314731391770942433625992710475394021675572575027445852371400736509772725581130537614203735350104770971283827769016324589620678432160581245381480093375303381611323
q = 34857423162121791604235470898471761566115159084585269586007822559458774716277164882510358869476293939176287610274899509786736824461740603618598549945273029479825290459062370424657446151623905653632181678065975472968242822859926902463043730644958467921837687772906975274812905594211460094944271575698004920372905721798856429806040099698831471709774099003441111568843449452407542799327467944685630258748028875103444760152587493543799185646692684032460858150960790495575921455423185709811342689185127936111993248778962219413451258545863084403721135633428491046474540472029592613134125767864006495572504245538373207974181

phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(c, d, n)

print(long_to_bytes(m))
```


### Kết quả

Chạy đoạn code trên thu được:

```text
b'crypto{I_want_to_Break_Square-free_4p-1}'
```

Vậy flag là:

```text
crypto{I_want_to_Break_Square-free_4p-1}
```

---
<img width="503" height="106" alt="image" src="https://github.com/user-attachments/assets/85f60a63-66a0-4136-965a-699ceb53fa93" />


## **23. Bespoke Padding**

### Given
Bài toán yêu cầu giải mã một thông điệp RSA có sử dụng padding tùy chỉnh. Mỗi lần mã hóa, flag được mã hóa với một padding khác nhau.

#### Tham số
- **p, q**: Hai số nguyên tố 1024 bit được sử dụng để tạo ra modulus `N`.
- **N**: Là tích của hai số nguyên tố `p` và `q`, tức là `N = p * q`.
- **e**: Số mũ công khai (`e = 11`).
- **FLAG**: Cờ mà bạn cần giải mã, có định dạng `crypto{???????????????????????????}`.
  
### Goal
Mỗi lần bạn yêu cầu mã hóa flag, một padding ngẫu nhiên được áp dụng vào thông điệp. Padding này được tạo ra từ hai số nguyên ngẫu nhiên `a` và `b`, và thông điệp sẽ được mã hóa theo phương thức:

\[
m = text{bytes\_to\_long}(text{flag})
\]
\[
text{pad\_msg} = a cdot m + b
\]

Sau đó, thông điệp đã padding được mã hóa theo công thức:

\[
text{encrypted} = text{pow}(text{pad\_msg}, e, N)
\]

### Solution

1. **Tạo khóa RSA**: Khóa RSA được tạo từ hai số nguyên tố `p` và `q`.
2. **Áp dụng padding**: Mỗi lần mã hóa, padding ngẫu nhiên được áp dụng vào flag. Điều này có nghĩa là flag mã hóa mỗi lần sẽ khác nhau.
3. **Giải mã thông điệp**: Vì padding được tạo ra ngẫu nhiên, bạn cần tìm cách khôi phục thông điệp ban đầu từ dữ liệu đã mã hóa.

#### Phân tích và tấn công
Dữ liệu nhận được bao gồm:
- `encrypted_flag`: Dữ liệu đã được mã hóa.
- `modulus`: Giá trị `N`.
- `padding`: Các giá trị padding ngẫu nhiên.

Mục tiêu là sử dụng các giá trị này để khôi phục được thông điệp ban đầu (flag).

### Code tìm FLAG
```python
import socket
import json

# Kết nối tới server
HOST = 'socket.cryptohack.org'
PORT = 13386

def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'{"option":"get_flag"}')
        response = s.recv(1024)
        return json.loads(response)

# Lấy dữ liệu đã mã hóa từ server
data = connect_to_server()

# In ra encrypted flag và modulus
encrypted_flag = data["encrypted_flag"]
N = data["modulus"]
padding = data["padding"]


print("Encrypted flag:", encrypted_flag)
print("Modulus:", N)
print("Padding:", padding)
```
Code tìm FLAG

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a.monic()

def FranklinReiter(c1, c2, e, n, a1, b1, a2, b2):
    P.<X> = PolynomialRing(Zmod(n))

    g1 = (a1*X + b1)^e - c1
    g2 = (a2*X + b2)^e - c2

    return int(-gcd(g1, g2).coefficients()[0])

c1 = 2878541770875479700538980645022489052652779838963883862268026817166426417039919463236963390507307046326634703872280537467067742696639787192609769488919052545419119190066398990783581947278798037910506277397947588285998093950003094089963329770140593314668635940754481257775804384229002369671108815582459118647674550606119347487983453986281116009756152816183799880182210660978656475507140675089458058265971296259258268207468501053946378749643676641269894890364588680663491615255661967214865581346385880401292197870553292664912420303380215004099980768844056280656081194235775166437263428384802474463548807865519344521028

c2 = 9358116384757608317220706970044933224234531757534430486726495081731537172532063758197094588560146034813412820720481673323181357275640282880376945873337874973608627166040471894089735428062869998336412925856834427099792181042190148866392208300871274345910645764652104826046243088695635872852698560499075328079478071928766314699067332677717903138094289636247404854454155325144516881573563576396070030232748258930392036341155059002641951617271533252090371171187191825436351873340387567232507741852632380312374845945384752378753935677949921080187872070947832676605655712908147214739222055430858304648290542768856843645161

e = 11

n = 16513150273488745819758318945465445929427923282220617948474026697826072849884410433840317590291164590606301920878166306100629001336979045875926362238578877426428184209782068217841561698268893281207281022882628671580544409079132228424570385789433865951296976542047938069538555185200454754405301473879058577591483273300132065945439952689462632448969760015421522358978863572507758617514279307992113676688788987384767873531588463072087737583220686506915075364580958023186096333340049114487946232564769897595127600679061991858554499358945100335619986316126901367151757694773827038242005563689706140134277497279550923802163

a1 = 12971547059542234095294614655038910108921383446804620937171913894104315123703020491747060634311615668108873604447661547527993522223132139978046365817767051166630231776636365059125563542171499632449531108005444897410900841477831293648565180438324816667994353072194547726135161768865833107935141472738129346943372760468854044004065874712379448469666278516423795881542818175602189759347359757114386437400569740686015395353195882174948910859334443292433002434909568745424239403127792523066229466813140793214725997586482270739634637321902855765823212470124155976347852151938219301641131781157846722399123723376114259029831

a2 = 11409457140242466819163427817479072385139033365230083718720047264434436898214384335636243055021460155275438092319802238955038605523688684385782916051156548581280516100417363773915481622407579450827246375873096305332208931991092735076355137904037100203515185779188885309077402419365710423222478825278182913737894421462042257973730289813359764845540728250586938424240047843075625738262558218714938963842910308398862881421355607305564841378461460037006115341626297306517807910746289965299025224005310222545925383605068291719567837393218166944929863737910844485524823699490307277435416628863671298960857171783974953402062

b1 = 613773303374507022635125910125983319338750375401989130365990413259288154566000703324060713319607895380155378987796575897467664632420947636683945281102489734850754988807647012567280983450240026466967889841627553095079976456551370938474121254303474971902286679389596876001000910960884922282188621864881761290594293008441025880989824356804970700431082846079890191931506602887887043528887971319087988804158703119751734009927979973925960770863614397143971164317388792822866081412005500649012213609335946463233073780263602030911938670236561006470408586945289329597277998553381709448864453473541694078648267392748834582252

b2 = 7245336764065642365831393452728740971259540086539413152250152735097680656770883053121301756868403120057747916744486252696211015549651622729853667084757925620818125696929068279230499982176189345006819380287349525312659226629850801073542291406883057493574547827172032691058542944679744377049745014959702974586433436512158229732186188003523586580642660072595199641524912132047912202451913864667343923032170547546966317318202888765453746148175214759547020579293565449701710859329968082044811127071473458891831112124821354298656439918625782443712556979595318257093732638944778996223990718369734263769019010362606613357004

flag = FranklinReiter(c1, c2, e, n, a1, b1, a2, b2)

print(bytes.fromhex(hex(flag)[2:]).decode())
```

FLAG: crypto{linear_padding_isnt_padding}
<img width="1496" height="405" alt="image" src="https://github.com/user-attachments/assets/e905da8b-2da3-4e72-a3b6-460de4baf5b6" />



## **24. Null or Never**

### Given
Bài toán yêu cầu giải mã thông điệp đã được mã hóa RSA sử dụng một phương thức padding tùy chỉnh. Mỗi lần mã hóa, padding sẽ được áp dụng để đảm bảo rằng thông điệp có độ dài cố định. Padding được sử dụng là padding `\x00`, có chiều dài 100 byte.

#### Tham số
- **n**: Modulus được tạo ra từ hai số nguyên tố `p` và `q` (RSA key).
- **e**: Mũ công khai (`e = 3`).
- **c**: Dữ liệu mã hóa (ciphertext) được sinh từ thông điệp đã padding.

### Goal
- Thông điệp được padding sao cho độ dài luôn bằng 100 byte. Điều này có thể tạo ra một số vấn đề bảo mật, vì thông điệp ban đầu có thể dễ dàng bị đoán nếu ta biết cách padding.
- Với padding `\x00`, thông điệp mã hóa có thể có những đặc điểm giúp ta giải mã hoặc rút ra được thông tin về flag.

### Solution

#### 1. Phân tích mã hóa RSA
Dữ liệu mã hóa (`c`) được sinh từ phương pháp RSA, với thông điệp đã padding và sử dụng công thức:

\[
c = m^e \mod n
\]

Trong đó `m` là thông điệp đã padding. Vì `e = 3`, ta cần phải xem liệu có thể khai thác padding này để giảm số khả năng cần kiểm tra.

#### 2. Phương pháp padding
Padding được thực hiện sao cho thông điệp luôn có độ dài là 100 byte, và tất cả byte dư sẽ được thay thế bằng `\x00`. Do đó, việc phân tích padding có thể giúp ta đoán được giá trị của `m`.

#### 3. Giải mã
Để giải mã, ta cần sử dụng các phương pháp tấn công RSA, đặc biệt là với **e = 3**. Một cách để giải mã là thử khai thác đặc điểm của padding và sử dụng công thức giải mã RSA:

\[
m = c^d \mod n
\]

Trong đó `d` là chỉ số riêng tư và được tính là nghịch đảo của `e` modulo `φ(n)`.

#### 4. Khai thác giá trị `m`
Vì padding là `\x00` và thông điệp có độ dài cố định, ta có thể thử các cách khai thác để tìm giá trị ban đầu của thông điệp `m`, sau đó chuyển đổi `m` sang byte để lấy flag.

### Code tìm FLAG
```python
from Crypto.Util.number import bytes_to_long, long_to_bytes
from CryptoHack_PGCD import PGCD_extended

FLAG = b"crypto{???????????????????????????????????}"
FLAG_min = b"crypto{!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!}"
FLAG_max = b"crypto{zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz}"

def lrackd(n, k=2):
    signe = +1
    if n < 2:
        if n < 0:
            if k % 2 == 0:
                raise ValueError("Erreur: racine paire d'un nombre négatif")
            else:
                signe, n = -1, abs(n)
        else:
            return n

    rac1, i = 1, 1
    while i <= n:
        rac1 <<= 1
        i <<= k

    rac2 = rac1
    rac1 >>= 1

    while rac1 != rac2:
        r = (rac1 + rac2) >> 1
        rn = r ** k

        if rn > n:
            rac2 = r
        else:
            rac1 = r + 1

        if n - rn < 0:
            r -= 1
    if signe > 0:
        return r
    return -r

def pad100(msg):
    return msg + b'\x00' * (100 - len(msg))

n = 95341235345618011251857577682324351171197688101180707030749869409235726634345899397258784261937590128088284421816891826202978052640992678267974129629670862991769812330793126662251062120518795878693122854189330426777286315442926939843468730196970939951374889986320771714519309125434348512571864406646232154103
e = 3
c = 63476139027102349822147098087901756023488558030079225358836870725611623045683759473454129221778690683914555720975250395929721681009556415292257804239149809875424000027362678341633901036035522299395660255954384685936351041718040558055860508481512479599089561391846007771856837130233678763953257086620228436828

pad = 256**((100-len(FLAG)))
c_pad = pow(pad, e, n)
r, u, v = PGCD_extended(c_pad, n)
c_pad_inv = u

assert (c_pad * c_pad_inv) % n == 1

flag_cube = (c * c_pad_inv) % n

m = bytes_to_long(FLAG_min)
c_flag_min = pow(m, e)

print('c_flag_min**e/n =', c_flag_min // n)

m = bytes_to_long(FLAG_max)
c_flag_max = pow(m, e)

print('c_flag_max**e/n =', c_flag_max // n)

n_time = c_flag_min // n

c_flag_decrypt = lrackd(flag_cube + n_time * n, 3)

print(long_to_bytes(c_flag_decrypt))
```
<img width="1488" height="389" alt="image" src="https://github.com/user-attachments/assets/931cf859-6d45-4402-9fe2-5cd4d1eccc8c" />

FLAG:
crypto{n0n_574nd4rd_p4d_c0n51d3r3d_h4rmful}



## **25. Signing Server**

### Given

- Trong hệ mật mã RSA nguyên thủy (Textbook RSA), phép toán tạo chữ ký điện tử (Digital Signature) và phép toán giải mã (Decryption) là hoàn toàn đồng nhất về mặt toán học. 
- Cụ thể, để ký một thông điệp $m$, hệ thống tính toán $s \equiv m^d \pmod N$. 
- Tương tự, để giải mã một bản mã $c$, hệ thống tính $m \equiv c^d \pmod N$. 
- Do đó, một hệ thống tự động ký các thông điệp bất kỳ bằng khóa bí mật $d$ (Signing Oracle) có thể bị lợi dụng như một hệ thống giải mã (Decryption Oracle).

Dữ kiện bài toán: Phân tích mã nguồn (13374.py) cho thấy máy chủ cung cấp giao diện tương tác JSON với 3 chức năng chính:
+ get_pubkey: Cung cấp tham số khóa công khai gồm module $N$ và số mũ $e$.
+ get_secret: Mã hóa cờ bí mật bằng khóa công khai và trả về bản mã $c \equiv secret^e \pmod N$.
+ sign: Nhận một thông điệp đầu vào dạng hex, thực thi phép ký bằng khóa bí mật và trả về kết quả $s \equiv msg^d \pmod N$.
### Goal

- Khai thác điểm yếu cấu trúc của hàm sign, sử dụng nó như một công cụ giải mã (Decryption Oracle) để khôi phục bản mã nhận được từ hàm get_secret về định dạng văn bản gốc (Flag).

### Solution

Lỗ hổng cốt lõi của máy chủ này là việc thực thi phép ký trực tiếp lên dữ liệu đầu vào mà không qua bước băm (hashing) hay đệm (padding) định dạng an toàn.

```python
from pwn import * # pip install pwntools
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes
import codecs
import base64

r = remote('socket.cryptohack.org', 13374, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

r.recvline()
json_send({"option": "get_secret"})
se = json_recv()
print(se)
json_send({"option": "sign", "msg": se["secret"]})
received = json_recv()
print(bytes.fromhex(received["signature"][2:]))
```
Kết quả: `crypto{d0n7_516n_ju57_4ny7h1n6}`



## **26. Let's Decrypt**

### Given

Hệ thống yêu cầu xác thực quyền sở hữu domain bằng chữ ký số RSA. Phân tích mã nguồn cho thấy hai điểm quan trọng:
+ Hệ thống cung cấp sẵn một chữ ký điện tử ($signature$) hợp lệ thông qua hàm get_signature.
+ Hàm verify mắc lỗi thiết kế nghiêm trọng: Cho phép người dùng tự định nghĩa khóa công khai (nhập tùy ý tham số module $N$ và số mũ $e$) để xác thực thông điệp.


### Goal

Tạo ra một thông điệp ($msg$) theo yêu cầu (chứa chuỗi I am Mallory...) và đánh lừa hệ thống chấp nhận $signature$ cũ là chữ ký hợp lệ cho $msg$ này bằng cách thao túng $N$ và $e$.

### Solution

Cơ chế kiểm tra chữ ký của máy chủ dựa trên phương trình:
$$signature^e \equiv digest \pmod N$$(Trong đó $digest$ là giá trị băm PKCS#1 v1.5 của thông điệp $msg$ ta gửi lên).
Vì ta hoàn toàn kiểm soát $N$ và $e$, ta có thể vô hiệu hóa độ khó của RSA bằng cách đặt số mũ $e = 1$. Phương trình được đơn giản hóa thành:$$signature \equiv digest \pmod N$$Theo tính chất của phép chia lấy dư, để $signature$ chia cho $N$ dư $digest$, ta chỉ cần thiết lập module $N = signature - digest$. Mọi thứ sẽ tự động khớp hoàn hảo mà không cần phải giải mã hay bẻ khóa hệ thống.

```python
from pwn import *
import json
from Crypto.Util.number import bytes_to_long
from pkcs1 import emsa_pkcs1_v15

io = remote("socket.cryptohack.org", 13391, level='error')

def json_send(hsh):
    io.sendline(json.dumps(hsh).encode())

def json_recv():
    return json.loads(io.recvline().decode())

io.recvline()

json_send({"option": "get_signature"})
data = json_recv()
sig = int(data["signature"], 16)

msg = "I am Mallory own CryptoHack.org"
digest = emsa_pkcs1_v15.encode(msg.encode(), 256)
digest_int = bytes_to_long(digest)

e = 1
n = sig - digest_int

json_send({
    "option": "verify",
    "msg": msg,
    "N": hex(n),
    "e": hex(e)
})

print(f"{json_recv()}")
```


> Kết quả:
`crypto{dupl1c4t3_s1gn4tur3_k3y_s3l3ct10n}`

 

## **27. Blinding Light**

### Given
  
  - Hệ thống cho phép ký (sign) mọi thông điệp, ngoại trừ thông điệp chứa chuỗi admin=True. 
  - Để lấy Flag, ta cần cung cấp chữ ký hợp lệ cho chính chuỗi admin=True này trong hàm verify.

### Goal

Lợi dụng tính chất "đồng cấu nhân" (multiplicative homomorphic) của RSA để tạo ra chữ ký cho thông điệp admin=True mà không cần gửi trực tiếp thông điệp này cho hệ thống ký.

### Solution

RSA bảo toàn phép nhân: $(m_1 \cdot m_2)^d \equiv m_1^d \cdot m_2^d \pmod N$.
Nghĩa là, chữ ký của một tích bằng tích của các chữ ký. Ta thực hiện các bước sau:
- Chuyển chuỗi admin=True thành số nguyên $m = 459922107199558918501733$.
- Phân tích $m$ thành 2 thừa số nguyên tố nhỏ (có thể dùng sympy hoặc tra FactorDB):$p_1 = 211578328037$$p_2 = 2173767566209$ (Lúc này $m = p_1 \cdot p_2$, và cả $p_1, p_2$ đều không chứa chuỗi admin=True).
- Yêu cầu server ký riêng lẻ $p_1$ (được $S_1$) và $p_2$ (được $S_2$).
- Chữ ký hợp lệ cho admin=True chính là $S = S_1 \cdot S_2 \pmod N$.

```python
from pwn import *
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes

io = remote('socket.cryptohack.org', 13376, level='error')

def json_send(hsh):
    io.sendline(json.dumps(hsh).encode())

def json_recv():
    return json.loads(io.recvline())

io.recvline()

json_send({"option": "get_pubkey"})
N = int(json_recv()['N'], 16)

p1 = 211578328037
p2 = 2173767566209

json_send({"option": "sign", "msg": long_to_bytes(p1).hex()})
s1 = int(json_recv()['signature'], 16)

json_send({"option": "sign", "msg": long_to_bytes(p2).hex()})
s2 = int(json_recv()['signature'], 16)

admin_signature = (s1 * s2) % N

json_send({
    "option": "verify",
    "msg": b"admin=True".hex(),

    "signature": hex(admin_signature)
})

print(f"{json_recv()['response']}")
```

> Kết quả: 
`crypto{m4ll34b1l17y_c4n_b3_d4n63r0u5}`




## **28. Vote for Pedro**

### Given

- Hệ thống yêu cầu xác thực 3 thông điệp khác nhau để thu thập 3 mảnh ghép (shares). Các mảnh này khi XOR lại với nhau sẽ tạo thành Flag.
- Ta vẫn được quyền tự set khóa công khai $N$ (với điều kiện không được là số nguyên tố), nhưng có một rào cản lớn: Ta phải gửi $N$ trước. Sau khi chốt $N$, server mới trả về một chuỗi suffix ngẫu nhiên và bắt buộc mọi thông điệp phải kết thúc bằng chuỗi này.
- Vì suffix làm thay đổi hoàn toàn giá trị băm (digest $D$) của thông điệp sau khi đã chốt $N$, trick "ăn gian" $N = S - D$ ở bài trước đã bị vô hiệu hóa.2. Goal
### Goal

Tìm ra một module $N$ có cấu trúc đặc biệt sao cho: Dù giá trị băm $D$ có sinh ra là số nào đi chăng nữa, ta vẫn có thể giải bài toán Logarit Rời Rạc (Discrete Logarithm Problem): $S^e \equiv D \pmod N$ một cách nhanh chóng để tìm ra số mũ $e$.

### Solution

Quy trình khai thác:
1. Lấy chữ ký $S$ từ server. Tìm một số nguyên tố nhỏ $p$ (ví dụ $p=3$) mà $S$ không chia hết cho $p$.
2. Đặt $N = p^{1000}$ (một con số khổng lồ nhưng vô dụng về mặt bảo mật) gửi lên server để nhận suffix.
3. Tạo thông điệp ghép với suffix. Nếu cần thiết, thêm bớt một vài khoảng trắng (space) vào thông điệp cho đến khi giá trị băm $D$ thỏa mãn điều kiện toán học.
4. Dùng SageMath (chuyên gia xử lý toán học) để tính trực tiếp số mũ $e$.
5. Lấy 3 mảnh ghép và XOR ra Flag.

```python
bytes2long = lambda x: int.from_bytes(x, 'big')

x = mod(bytes2long(b"VOTE FOR PEDRO"), 2**120).nth_root(3)

print('{' + f'"option":"vote","vote":"{hex(x)[2:]}"' + '}')
```
Sau khi chạy đoạn code trên ta có được: `{"option":"vote","vote":"a4c46bfb65e7eccc4e76a1ce2afc6f"}`

-> Kết nối tới Server và gửi cho nó
> Kết quả:
`crypto{y0ur_v0t3_i5_my_v0t3}`


## **29. Let's Decrypt Again**

### Given

- Hệ thống yêu cầu xác thực 3 thông điệp khác nhau để nhận 3 mảnh bí mật (shares), XOR 3 mảnh này sẽ ra Flag.
- Máy chủ bắt buộc ta gửi module $N$ trước. Sau đó, máy chủ sinh ra một chuỗi suffix ngẫu nhiên và bắt buộc nối vào đuôi mọi thông điệp. Điều này vô hiệu hóa việc tính toán trước giá trị băm $D$ để gài $N$.

### Goal

- Lựa chọn một module $N$ có cấu trúc toán học đặc biệt yếu để biến bài toán Logarit Rời Rạc (Discrete Logarithm Problem - DLP) từ "không thể giải" thành "giải trong tích tắc". 
- Từ đó, với bất kỳ giá trị băm $D$ nào sinh ra từ suffix, ta đều tính ngược được số mũ $e$.

### Solution

- Điểm yếu cốt lõi là máy chủ chỉ kiểm tra $N$ không phải là số nguyên tố, nhưng không cấm $N$ là lũy thừa của một số nguyên tố ($N = p^k$).
- Khi chọn $p$ là một số nguyên tố (ví dụ $p = 2010103$) và $k$ đủ lớn ($k = 50$), cấu trúc của nhóm nhân modulo $N$ trở nên cực kỳ yếu. 
- Ta có thể sử dụng hàm discrete_log của SageMath để giải phương trình $S^e \equiv D \pmod N$ một cách trực tiếp.

```python
from pwn import *
from json import dumps, loads
from Crypto.Util.number import bytes_to_long
from pkcs1 import emsa_pkcs1_v15
from sage.all import Mod, discrete_log

r = remote('socket.cryptohack.org', 13394)
r.recvline()

r.sendline(dumps({'option': 'get_signature'}).encode())
s = int(loads(r.recvline())['signature'], 16)

p, k = 2010103, 50
n = p**k
r.sendline(dumps({'option': 'set_pubkey', 'pubkey': hex(n)}).encode())
suffix = loads(r.recvline())['suffix']

m1 = 'This is a test for a fake signature.' + suffix
m2 = 'My name is Zupp and I own CryptoHack.org' + suffix
m3 = 'Please send all my money to 3EovkHLK5kkAbE8Kpe53mkEbyQGjyf8ECw' + suffix

def cvt(msg):
    return bytes_to_long(emsa_pkcs1_v15.encode(msg.encode(), 768 // 8))

msg1, msg2, msg3 = cvt(m1), cvt(m2), cvt(m3)

s_mod = Mod(s, n)
e1 = discrete_log(Mod(msg1, n), s_mod)
e2 = discrete_log(Mod(msg2, n), s_mod)
e3 = discrete_log(Mod(msg3, n), s_mod)

def claim(msg, idx, e_val):
    r.sendline(dumps({'option': 'claim', 'msg': msg, 'index': idx, 'e': hex(e_val)}).encode())
    return bytes.fromhex(loads(r.recvline())['secret'])

sec1 = claim(m1, 0, e1)
sec2 = claim(m2, 1, e2)
sec3 = claim(m3, 2, e3)

flag = xor(sec1, sec2, sec3).decode()
print(f"{flag}")
```
> Kết quả: 
`crypto{let's_decrypt_w4s_t0o_ez_do_1t_ag41n}`




