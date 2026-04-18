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