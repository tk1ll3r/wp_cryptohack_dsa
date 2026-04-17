from pwn import *
import json

r = remote('socket.cryptohack.org', 13374, level='error')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

r.recvline()

json_send({"option": "get_secret"})
secret_data = json_recv()
ciphertext = secret_data["secret"]
print(f"[*] Nhận được bản mã: {ciphertext[:30]}...")

json_send({"option": "sign", "msg": ciphertext})
signed_data = json_recv()

signature_hex = signed_data["signature"]
if signature_hex.startswith("0x"):
    signature_hex = signature_hex[2:]

flag = bytes.fromhex(signature_hex).decode('utf-8')
print(f"{flag}")