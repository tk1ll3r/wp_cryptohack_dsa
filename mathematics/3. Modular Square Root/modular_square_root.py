import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "output.txt")

with open(file_path, "r") as f:
    content = f.read()

for line in content.strip().split("\n"):
    if line.startswith("p ="):
        p = int(line.split("=", 1)[1].strip())
    elif line.startswith("a ="):
        a = int(line.split("=", 1)[1].strip())

def tonelli_shanks(a, p):
    if pow(a, (p - 1) // 2, p) != 1:
        return None 

    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    Q, S = p - 1, 0
    while Q % 2 == 0:
        Q //= 2
        S += 1

    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1

    M = S
    c = pow(z, Q, p)     
    t = pow(a, Q, p) 
    R = pow(a, (Q + 1) // 2, p) 

    while True:
        if t == 1:
            return R 

        i, tmp = 1, pow(t, 2, p)
        while tmp != 1:
            tmp = pow(tmp, 2, p)
            i += 1

        b = pow(c, pow(2, M - i - 1), p)
        M = i
        c = pow(b, 2, p)
        t = (t * c) % p
        R = (R * b) % p

root  = tonelli_shanks(a, p)
root2 = p - root

assert pow(root,  2, p) == a % p
assert pow(root2, 2, p) == a % p

flag = min(root, root2)
print(flag)