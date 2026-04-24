import os
from Crypto.PublicKey import RSA

# Lấy đường dẫn thư mục của chính file script này
dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = "bruce_rsa_6e7ecd53b443a97013397b1a1ea30e14.pub"
full_path = os.path.join(dir_path, file_name)

with open(full_path, "r") as f:
    key = RSA.importKey(f.read())

print("Flag của bạn đây:")
print(key.n)