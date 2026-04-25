import ast
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "output.txt")

with open(file_path, "r") as f:
    content = f.read()

for line in content.strip().split("\n"):
    if line.startswith("p ="):
        p = int(line.split("=", 1)[1].strip())
    elif line.startswith("ints ="):
        ints = ast.literal_eval(line.split("=", 1)[1].strip())

qr = None
for x in ints:
    legendre = pow(x, (p - 1) // 2, p)
    if legendre == 1:
        qr = x
        break

assert p % 4 == 3, "Công thức này chỉ hoạt động khi p ≡ 3 (mod 4)"

root  = pow(qr, (p + 1) // 4, p)  
root2 = p - root        

assert pow(root,  2, p) == qr
assert pow(root2, 2, p) == qr

flag = max(root, root2)
print(flag)