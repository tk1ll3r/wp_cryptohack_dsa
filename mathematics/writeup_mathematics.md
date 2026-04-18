### Mathematics
---
> #### 11. Roll your Own

> Given

- Bài toán Discrete Logarithm (DLP) tìm $x$ từ phương trình $h \equiv g^x \pmod n$ được coi là rất khó giải nếu $n$ là một số nguyên tố lớn và nhóm có cấu trúc an toàn.
- Server cung cấp cho ta một số nguyên tố $q$ (512-bit). Điểm yếu chết người là server cho phép ta tự chọn cơ số $g$ và modulo $n$, với một điều kiện duy nhất:$$g^q \equiv 1 \pmod n$$
- Sau khi vượt qua vòng kiểm tra này, server sẽ chọn một số ngẫu nhiên $x$ trong khoảng $[0, q]$, tính public key $h = g^x \pmod n$ và gửi lại cho ta.

> Goal

Tìm ra tham số $g$ và $n$ phù hợp để "lách" qua bài kiểm tra của server, đồng thời biến phương trình $h \equiv g^x \pmod n$ thành một phương trình tuyến tính dễ giải để tìm lại khóa bí mật $x$.

> Solution
- Sử dụng Khai triển nhị thức (Binomial Expansion) kết hợp với một Modulo hợp số (Composite Modulus).
```python
from pwn import remote
from json import loads, dumps

import logging
logging.getLogger("pwnlib").setLevel(logging.ERROR)

HOST = 'socket.cryptohack.org'
PORT = 13403

def solve():
    r = remote(HOST, PORT)

    r.recvuntil(b"Prime generated: ")
    q_str = r.recvline().decode().strip()
    q = int(q_str.replace('"', ''), 16)

    g = q + 1
    n = q ** 2
    
    payload_params = {
        "g": hex(g),
        "n": hex(n)
    }

    r.recvuntil(b"Send integers (g,n) such that pow(g,q,n) = 1: ")
    r.sendline(dumps(payload_params).encode())
    r.recvuntil(b"Generated my public key: ")
    h_str = r.recvline().decode().strip()
    h = int(h_str.replace('"', ''), 16)
    x = (h - 1) // q
    payload_secret = {
        "x": hex(x)
    }
    r.recvuntil(b"What is my private key: ")
    r.sendline(dumps(payload_secret).encode())

    response = r.recvline().decode().strip()
    try:
        flag = loads(response)['flag']
        print(f"{flag}")
    r.close()

if __name__ == '__main__':
    solve()
```
> Kết quả:
`crypto{Grabbing_Flags_with_Pascal_Paillier}`

---
> #### 12. Unencryptable

> Given

- Theo output của file output.txt, khi chạy hàm encrypt(DATA, e, N), hệ thống đã in ra dòng chữ "RSA broken!?".
- Nhìn vào mã nguồn hàm encrypt, dòng chữ này chỉ được in ra khi bản mã bằng đúng bản rõ:$$m^e \equiv m \pmod N$$
- Điều này có nghĩa là biến DATA ($m$) là một điểm cố định (fixed point) của khóa public này. Nó đi qua hàm mã hóa nhưng không hề bị thay đổi.

> Goal

- Lợi dụng tính chất $m^e \equiv m \pmod N$ của biến DATA để phân tích thừa số nguyên tố modulo $N$ (tìm ra $p$ và $q$). 
- Sau khi có $p$ và $q$, ta dễ dàng tính được Private Key $d$ và giải mã biến encrypted_flag ($c$).

> Solution
```python
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse
from math import gcd

DATA = bytes.fromhex("372f0e88f6f7189da7c06ed49e87e0664b988ecbee583586dfd1c6af99bf20345ae7442012c6807b3493d8936f5b48e553f614754deb3da6230fa1e16a8d5953a94c886699fc2bf409556264d5dced76a1780a90fd22f3701fdbcb183ddab4046affdc4dc6379090f79f4cd50673b24d0b08458cdbe509d60a4ad88a7b4e2921")
N = 0x7fe8cafec59886e9318830f33747cafd200588406e7c42741859e15994ab62410438991ab5d9fc94f386219e3c27d6ffc73754f791e7b2c565611f8fe5054dd132b8c4f3eadcf1180cd8f2a3cc756b06996f2d5b67c390adcba9d444697b13d12b2badfc3c7d5459df16a047ca25f4d18570cd6fa727aed46394576cfdb56b41
e = 0x10001
c = 0x5233da71cc1dc1c5f21039f51eb51c80657e1af217d563aa25a8104a4e84a42379040ecdfdd5afa191156ccb40b6f188f4ad96c58922428c4c0bc17fd5384456853e139afde40c3f95988879629297f48d0efa6b335716a4c24bfee36f714d34a4e810a9689e93a0af8502528844ae578100b0188a2790518c695c095c9d677b

m = bytes_to_long(DATA)

p = 0
q = 0

if gcd(m, N) > 1 and gcd(m, N) != N:
    p = gcd(m, N)
    q = N // p
else:
    x = m
    for _ in range(16): # e - 1 = 65536 = 2^16, nên ta bình phương tối đa 16 lần
        next_x = pow(x, 2, N)
        if next_x == 1:
            if x != 1 and x != N - 1:
                p = gcd(x - 1, N)
                q = N // p
                break
        x = next_x

if p and q:
    print(f"[+] Tìm thấy p = {p}")
    print(f"[+] Tìm thấy q = {q}")
    
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    
    flag_int = pow(c, d, N)
    flag = long_to_bytes(flag_int).decode()
    
    print(f"{flag}")
```
> Kết quả
`crypto{R3m3mb3r!_F1x3d_P0iNts_aR3_s3crE7s_t00}`

---
> #### 13. Cofactor Cofantasy

> Given

- Modulo $N$ là tích của các "Safe Primes" (Số nguyên tố an toàn). Safe prime có dạng $p = 2q + 1$, với $q$ cũng là số nguyên tố.
- Do đó, $\phi(N) = \prod (p_i - 1) = \prod (2q_i) = 2^k \cdot \prod q_i$. Các giá trị $q_i$ thường rất lớn.
- Server cho phép lấy từng bit của Flag thông qua hàm get_bit(i).
- Nếu bit thứ $i$ bằng 1, nó trả về một số thuộc tập sinh bởi $g$: pow(g, r, N).Nếu bit thứ $i$ bằng 0, nó trả về một số hoàn toàn ngẫu nhiên: randint(1, N - 1)

> Goal

- Làm thế nào để phân biệt giữa một số $x = g^r \pmod N$ và một số ngẫu nhiên $y \pmod N$? Nếu phân biệt được, ta sẽ biết bit đó là 1 hay 0 và khôi phục toàn bộ Flag.

> Solution

- Bước 1: Phân tích tham số phi ($\phi$)Từ $N$ và $\phi(N)$ được cho trước, ta có thể tính được tổng các thừa số nguyên tố, nhưng điều quan trọng hơn là cấu trúc của $\phi$.Để ý rằng $\phi$ luôn chẵn (vì $p-1$ luôn chẵn). Nhóm nhân $\mathbb{Z}_N^*$ có cấp (order) là $\phi(N)$.
- Bước 2: Tìm "Order" của phần tử sinh $g$Bất kỳ phần tử nào dạng $g^r \pmod N$ đều thuộc nhóm con (subgroup) sinh bởi $g$. Kích thước của nhóm con này được gọi là bậc (order) của $g$, ký hiệu là $ord(g)$.Theo định lý Lagrange, $ord(g)$ phải là một ước của $\phi(N)$.Thủ thuật ở đây là tìm ra một số $k$ sao cho:$k$ là bội số của $ord(g)$.$k$ không phải là bội số của $\phi(N)$.Nếu có một số $k$ như vậy, thì đối với bất kỳ giá trị $x = g^r \pmod N$, ta luôn có:$$x^k \equiv (g^r)^k \equiv (g^{ord(g)})^{\text{something}} \equiv 1^{\text{something}} \equiv 1 \pmod N$$Ngược lại, đối với một số ngẫu nhiên $y$, xác suất để $y^k \equiv 1 \pmod N$ là cực kỳ thấp (vì $k$ không bao phủ toàn bộ $\phi(N)$).
- Bước 3: Tìm $k$ bằng CofactorTa có $\phi(N)$ và $N$. Bạn có thể phân tích $\phi(N)$ ra thừa số nguyên tố. Vì N cấu tạo từ safe primes, $\phi(N)$ sẽ có một lượng lớn thừa số 2.Thực tế, qua phân tích thuật toán, $g$ thường được chọn sao cho nó có bậc là một số lẻ lớn, hoặc thiếu đi một số thừa số nhỏ.Thay vì phân tích toàn bộ $\phi(N)$, ta thử lấy $\phi(N)$ chia cho các số nguyên tố nhỏ (2, 3, 5, 7...) để tạo ra một "Cofactor" $k$.Cụ thể, giả sử $g$ sinh ra nhóm con thiếu thừa số 2, ta kiểm tra $g^{\phi(N)//2} \pmod N$. Nếu nó bằng 1, ta chọn $k = \phi(N) // 2$.Thử nghiệm với dữ liệu bài toán, ta tìm được:$$k = \phi(N) // 2$$thỏa mãn $g^k \equiv 1 \pmod N$.- - Bước 4: Trích xuất FlagVới mỗi bit $i$:Gửi yêu cầu lấy giá trị $V$ cho bit $i$.Tính $T = V^k \pmod N$ với $k = \phi(N) // 2$.Nếu $T == 1$, bit đó là 1. Nếu $T \neq 1$, bit đó là 0.
```python
from pwn import *
import json

N = 56135841374488684373258694423292882709478511628224823806418810596720294684253418942704418179091997825551647866062286502441190115027708222460662070779175994701788428003909010382045613207284532791741873673703066633119446610400693458529100429608337219231960657953091738271259191554117313396642763210860060639141073846574854063639566514714132858435468712515314075072939175199679898398182825994936320483610198366472677612791756619011108922142762239138617449089169337289850195216113264566855267751924532728815955224322883877527042705441652709430700299472818705784229370198468215837020914928178388248878021890768324401897370624585349884198333555859109919450686780542004499282760223378846810870449633398616669951505955844529109916358388422428604135236531474213891506793466625402941248015834590154103947822771207939622459156386080305634677080506350249632630514863938445888806223951124355094468682539815309458151531117637927820629042605402188751144912274644498695897277
phi = 56135841374488684373258694423292882709478511628224823806413974550086974518248002462797814062141189227167574137989180030483816863197632033192968896065500768938801786598807509315219962138010136188406833851300860971268861927441791178122071599752664078796430411769850033154303492519678490546174370674967628006608839214466433919286766123091889446305984360469651656535210598491300297553925477655348454404698555949086705347702081589881912691966015661120478477658546912972227759596328813124229023736041312940514530600515818452405627696302497023443025538858283667214796256764291946208723335591637425256171690058543567732003198060253836008672492455078544449442472712365127628629283773126365094146350156810594082935996208856669620333251443999075757034938614748482073575647862178964169142739719302502938881912008485968506720505975584527371889195388169228947911184166286132699532715673539451471005969465570624431658644322366653686517908000327238974943675848531974674382848
g = 986762276114520220801525811758560961667498483061127810099097

k = phi
while k % 2 == 0:
    k //= 2

R = pow(g, k, N)
valid_roots = {1, R}

context.log_level = 'error' 
r = remote("socket.cryptohack.org", 13398)
r.recvline()

flag_bits = ""
i = 0
while True:
    is_bit_1 = True
    
    for _ in range(6):
        payload = json.dumps({"option": "get_bit", "i": i}).encode()
        r.sendline(payload)
        
        try:
            data = r.recvline()
            if not data: break
            response = json.loads(data.decode())
        except:
            break
            
        if "error" in response:
            break 
            
        val = int(response["bit"], 16)
        
        # Nếu chỉ cần 1 lần thử mà giá trị val^k lọt ra ngoài tập {1, R}
        if pow(val, k, N) not in valid_roots:
            is_bit_1 = False
            break 
            
    if "error" in response:
        break
        
    flag_bits += "1" if is_bit_1 else "0"
    i += 1

flag_bytes = []
for j in range(0, len(flag_bits), 8):
    byte_str = flag_bits[j:j+8]
    if len(byte_str) == 8:
        reversed_byte = byte_str[::-1]
        flag_bytes.append(int(reversed_byte, 2))

flag = bytes(flag_bytes)
print(f"{flag.decode(errors='ignore')}")

r.close()
```
> Kết quả
`crypto{0ver3ng1neering_ch4lleng3_s0lution$}`

---
> #### 14. Real Eisenstein

> Given

- Tác giả giấu Flag (độ dài 27 ký tự) bằng cách nhân mã ASCII của từng ký tự với căn bậc hai của 27 số nguyên tố đầu tiên, sau đó cộng dồn lại thành một số thực $h$:$$h = \sum_{i=0}^{26} char_i \times \sqrt{P_i}$$
- Làm tròn số: Để biến $h$ thành số nguyên (Ciphertext - ct), tác giả nhân nó với một hằng số cực lớn là $16^{64}$ (tương đương $2^{256}$) và áp dụng phép làm tròn xuống (floor):$$ct = \lfloor h \times 16^{64} \rfloor$$

> Goal

- Giải quyết bài toán Hidden Subset Sum (Tổng tập con bị giấu) trên tập số thực. 
- Ta cần khôi phục lại 27 biến $char_i$ (giá trị ASCII từ 32 đến 126) từ một tổng duy nhất $ct$.

> Solution

Quy về bài toán Knapsack (Cái túi): Nhờ phép nhân với $16^{64}$, các số thực đã được phóng to đủ lớn để xấp xỉ thành các số nguyên. Đặt $S_i = \lfloor \sqrt{P_i} \times 16^{64} \rfloor$, ta có phương trình tuyến tính:$$\sum_{i=0}^{26} char_i \times S_i \approx ct$$

```python
n = 27  
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]
ct = 1350995397927355657956786955603012410260017344805998076702828160316695004588429433
R = RealField(2048)
multiplier = R(16)^64

S = []
for p in PRIMES:
    val = (R(p).sqrt() * multiplier).floor()
    S.append(val)

M = Matrix(ZZ, n + 1, n + 1)
for i in range(n):
    M[i, i] = 1
    M[i, n] = S[i]

M[n, n] = ct
res = M.BKZ()
for row in res:
    try:
        # Lấy n phần tử đầu tiên, chuyển thành trị tuyệt đối và dịch ra mã ASCII
        flag = "".join(chr(abs(row[kk])) for kk in range(n))
        
        if "crypto{" in flag:
            print(f"{flag}")
            break
    except ValueError:
        continue
```
> Kết quả
`crypto{r34l_t0_23D_m4p}`


---
> #### 15. Prime and Prejudice

> Given

- Miller-Rabin Bypass: Hàm miller_rabin(n, 64) của server chỉ kiểm tra với các cơ số nguyên tố $b \le 61$.
- Do đó, ta có thể đánh lừa nó bằng một hợp số đặc biệt (Adversarial Carmichael Number) đóng vai trò là số nguyên tố giả.
- Logic rò rỉ Flag: Server tính $x = a^{p-1} \pmod p$ và trả về FLAG[:x]. 
- Nếu đưa vào số nguyên tố thật, theo Định lý nhỏ Fermat, $x$ luôn bằng $1$ (chỉ rò rỉ ký tự đầu tiên). Tuy nhiên, nếu $p$ là hợp số, $x$ sẽ là một con số khổng lồ, làm lộ toàn bộ Flag.

> Solution
- Xây dựng hợp số $N = p_1 \cdot p_2 \cdot p_3$ (có độ dài 600-900 bit) thỏa mãn tính chất Carmichael và đồng dư modulo 4 để vượt qua mọi phép thử Miller-Rabin $\le 61$.
- Chọn cơ số (base) $a = p_1$. Theo Định lý số dư Trung Hoa (CRT), $a^{N-1} \pmod N$ sẽ tạo ra một số rất lớn (tương đương $\frac{N}{p_1}$).
##### Tìm $N$ và $a$ bằng SageMath
```python
P = 8 * prod(list(primes(3, 64)))
rems = [7] + [1 if p % 4 == 1 else p - 1 for p in primes(3, 64)]
R = crt(rems, [8] + list(primes(3, 64)))

G = gcd(R - 1, P)
M = P // G

# Tìm hệ số a, b
ka = 2000
while True:
    a = ka * M + 1
    if gcd(a, P) == 1: break
    ka += 1

kb = ka + 1
while True:
    b = kb * M + 1
    if gcd(b, P) == 1 and gcd(b, a) == 1: break
    kb += 1
X_a = (-(b + 1) * inverse_mod(b, a)) % a
X_b = (-(a + 1) * inverse_mod(a, b)) % b

X0 = crt([R - 1, X_a, X_b], [P, a, b])
step = P * a * b
X = X0
attempts = 0
while True:
    attempts += 1
    p3 = X + 1
    
    if p3.is_prime(proof=False):
        p1 = a * X + 1
        if p1.is_prime(proof=False):
            p2 = b * X + 1
            if p2.is_prime(proof=False):
                break
    X += step

N = p1 * p2 * p3
print(f"prime = {N}")
print(f"base = {p1}")
```
##### Bước 2: Gửi lên Server bằng Python

```python
from pwn import remote
import json

HOST = 'socket.cryptohack.org'
PORT = 13385

ADVERSARIAL_PRIME = 41225151171984121525796110501918164585971821642266667055673150051163081385220756658858966634094565631783101689101523375411776517143302232523056241615631527689287857945551328797028679967247034416541409446751 
BASE_A = 49732030987493448887188691409582947539892185938129179647526576644613478791

r = remote(HOST, PORT)
r.recvline()

payload = {
    "prime": int(ADVERSARIAL_PRIME),
    "base": int(BASE_A)
}

r.sendline(json.dumps(payload).encode())

response = r.recvline().decode()
print(f"{response.strip()}")
r.close()

```
> Kết quả
`crypto{Forging_Primes_with_Francois_Arnault}`

