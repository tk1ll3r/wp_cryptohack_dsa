def extended_gcd(a, b):
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1
    
    while b != 0:
        q = a // b
        a, b = b, a % b
        
        
        x0, x1 = x1, x0 - q * x1 # Cập nhật hệ số x (tương ứng với u)
        
        
        y0, y1 = y1, y0 - q * y1 # Cập nhật hệ số y (tương ứng với v)
        
    return a, x0, y0 # a là gcd(p,q)

#---
p = 26513
q = 32321
gcd_val, u, v = extended_gcd(p, q)

flag = min(u, v)
print(flag)
