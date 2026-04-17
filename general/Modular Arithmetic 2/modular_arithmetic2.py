a = 273246787654
p = 65537

# Dùng hàm pow() để tính lũy thừa modulo
result = pow(a, p - 1, p)

print(result)