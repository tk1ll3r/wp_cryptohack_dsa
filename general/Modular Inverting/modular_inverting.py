def egcd(a, b):
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    
    # Trả về x0 - hệ số đi kèm với a ban đầu
    return x0
#---
m = 13
x0 = egcd(3, m)
#tính ra hệ số x0

#---
inverse = x0 % m # số x0 cần phải số dương trong khoảng [0, m-1]


print(inverse)