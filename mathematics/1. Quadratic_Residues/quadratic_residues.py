p = 29
ints = [14, 6, 11]

for x in ints:
    roots = [a for a in range(1, p) if pow(a, 2, p) == x]
    
    if roots:
        print(f"{x} là Quadratic Residue, căn bậc hai: {roots}, nhỏ nhất: {min(roots)}")
    else:
        print(f"{x} là Quadratic Non-Residue")