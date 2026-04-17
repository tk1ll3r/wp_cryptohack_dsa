def gcd(a, b):            
    if a < b:             
        a, b = b, a     # luôn cho số a > b;
        
    while b != 0:              
        a, b = b, a % b   # sử dụng thuật toán Euclid
    return a # a chính là UCLN
print(gcd(66528, 52920))