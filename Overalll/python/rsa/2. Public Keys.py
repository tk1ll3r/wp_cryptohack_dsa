M = 12
e = 65537
p = 17
q = 23

N = p * q 

C = pow(M, e, N)
print(f"N = {N}")
print(f"C = {C}")
