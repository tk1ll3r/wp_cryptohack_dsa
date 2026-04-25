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
