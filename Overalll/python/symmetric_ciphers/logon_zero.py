from pwn import *
from json import dumps, loads

HOST = 'socket.cryptohack.org'
PORT = 13399

def send_json(msg):
    r.sendline(dumps(msg).encode())

context.log_level = 'error'

r = remote(HOST, PORT)
r.recvline() 

exploit_token = b'\x00' * 28 

expected_password = "" 

attempts = 0

while True:
    attempts += 1
    
    send_json({'option': 'reset_password', 'token': exploit_token.hex()})
    r.recvline()

    send_json({'option': 'authenticate', 'password': expected_password})
    response_data = r.recvline()
    
    if not response_data:
        continue
        
    response = loads(response_data)['msg']
    
    if 'Welcome admin, flag: ' in response:
        break

        
    send_json({'option': 'reset_connection'})
    r.recvline()

r.close()