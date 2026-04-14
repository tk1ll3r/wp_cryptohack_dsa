### RSA
---
> #### 7. Factoring

> Given
- Hệ mật mã RSA hoạt động dựa trên một module $N$ được tạo ra bằng cách nhân hai số nguyên tố bí mật $p$ và $q$ ($N = p \cdot q$). Tính bảo mật của RSA phụ thuộc hoàn toàn vào việc máy tính rất khó để phân tích $N$ ngược lại thành $p$ và $q$ nếu module đó đủ lớn.
- Hệ thống cung cấp một module $N$ có kích thước khá nhỏ (150-bit):
$N = 510143758735509025530880200653196460532653147$

> Goal

Phân tích module $N$ thành hai thừa số nguyên tố $p$ và $q$. Cờ (Flag) chính là số nguyên tố có giá trị nhỏ hơn.

> Solution

Sử dụng các công cụ trực tuyến để phân tích, ở bài này mình sử dụng `FactorDB.com` để tìm ra được só o nguyên tố.
![Kết quả](factory1.png)
> Và kết quả được mình lấy từ trang web: 
`19704762736204164635843`
 
---
> #### 8. Inferius Prime

> Given
- Cơ sở: Độ an toàn của hệ mật mã công khai RSA phụ thuộc hoàn toàn vào độ phức tạp tính toán của bài toán phân tích nhân tử số nguyên lớn (Integer Factorization Problem - IFP). Theo các tiêu chuẩn an toàn thông tin hiện hành, module $N$ đòi hỏi kích thước tối thiểu từ 2048-bit để chống lại các kỹ thuật phân tích hiện đại.
- Hệ thống cung cấp cấu hình khóa công khai bao gồm số mũ $e = 65537$, bản mã $ct$ và module $N$. Phân tích thực nghiệm cho thấy module $N$ chỉ sở hữu xấp xỉ 60 chữ số thập phân (tương đương với không gian khoảng 200-bit). Sự sai lệch tham số này là một điểm yếu nghiêm trọng trong khâu khởi tạo, làm suy giảm hoàn toàn tính an toàn của hệ mật mã.

>Goal

Phân tích module $N$ thành 2 số nguyên tố $p$ và $q$. Sau đó, sử dụng $p$ và $q$ để tính khóa bí mật $d$ và giải mã ciphertext $ct$ về dạng văn bản (Flag).

> Solution

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

![Kết quả](inferius_prime.png)

--- 
> #### 9. Monoprime

> Given

- Trong hệ mật mã RSA tiêu chuẩn, module $N$ được thiết lập từ tích của hai số nguyên tố phân biệt ($N = p \cdot q$). Dựa trên đặc tính này, phi hàm Euler (Euler's Totient function) được tính bằng công thức $\phi(N) = (p-1)(q-1)$.
- Tuy nhiên, hệ thống "Monoprime" này mắc một lỗi thiết kế kiến trúc cơ bản: module $N$ được cấu tạo từ một số nguyên tố duy nhất ($N = p$). Sự biến đổi này phá vỡ hoàn toàn bài toán phân tích nhân tử, vốn là nền tảng bảo mật của RSA.
- Bài toán cung cấp bộ tham số khóa công khai gồm số mũ $e = 65537$, bản mã $ct$ và một module $N$ siêu lớn nhưng bản thân nó đã là một số nguyên tố.
> Goal

- Khai thác lỗ hổng cấu trúc của module $N$ để tính toán trực tiếp phi hàm Euler $\phi(N)$, qua đó suy xuất khóa giải mã bí mật $d$ và khôi phục bản mã $ct$ về định dạng văn bản (Flag).

> Solution

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

![Kết quả](/crypto/rsa/MonoPrime/monoprime.png)


--- 
> #### 10. Square Eyes

> Given
- Trong quá trình sinh khóa RSA tiêu chuẩn, module $N$ bắt buộc phải là tích của hai số nguyên tố phân biệt ($N = p \cdot q$). 
- Dựa trên định lý cơ bản của số học, phi hàm Euler cho cấu trúc này là $\phi(N) = (p-1)(q-1)$. 
- Tuy nhiên, ở bài toán này, kiến trúc hệ thống đã bị thay đổi: module $N$ được thiết lập bằng bình phương của một số nguyên tố duy nhất ($N = p^2$). Khi cấu trúc vi phạm quy tắc này, công thức tính phi hàm Euler thay đổi. 
- Theo định lý toán học đối với lũy thừa của một số nguyên tố $p^k$, ta có $\phi(p^k) = p^k - p^{k-1}$. Do đó, với $k=2$, phi hàm được xác định bằng: $\phi(N) = p^2 - p = p(p-1)$.
- Hệ thống cung cấp bản mã $ct$, số mũ $e = 65537$ và một module $N$ khổng lồ (khoảng 4096-bit). Tác giả xác nhận rằng $N$ được tạo ra bằng cách lấy một số nguyên tố 2048-bit và "nhân nó với chính nó" (dùng hai lần).

> Goal

- Khai thác điểm yếu cấu trúc của module $N = p^2$ bằng thuật toán khai căn bậc hai số nguyên (Integer Square Root) để tìm lại tham số $p$. 
- Sau đó, áp dụng đúng định lý phi hàm Euler cho lũy thừa số nguyên tố để tính toán khóa giải mã $d$ và khôi phục văn bản gốc.

> Solution

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

![Kết quả](/crypto/rsa/square_eyes/square_eyes.png)

