import socket
import json

# Kết nối tới server
HOST = 'socket.cryptohack.org'
PORT = 13386

def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'{"option":"get_flag"}')
        response = s.recv(1024)
        return json.loads(response)

# Lấy dữ liệu đã mã hóa từ server
data = connect_to_server()

# In ra encrypted flag và modulus
encrypted_flag = data["encrypted_flag"]
N = data["modulus"]
padding = data["padding"]


print("Encrypted flag:", encrypted_flag)
print("Modulus:", N)
print("Padding:", padding)
