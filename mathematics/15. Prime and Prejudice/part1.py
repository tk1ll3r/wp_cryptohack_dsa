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
