import json
import socket

HOST = "socket.cryptohack.org"
PORT = 11112

s = socket.create_connection((HOST, PORT))
f = s.makefile("rw")

for _ in range(4):
    print(f.readline().strip())

request = {"buy": "flag"}
payload = json.dumps(request) + "\n"
f.write(payload)
f.flush()

response = f.readline()
print("-" * 20)
print(f"Server response: {response.strip()}")
print("-" * 20)

s.close()
