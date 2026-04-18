import socket
import json
import base64
import codecs

HOST = "socket.cryptohack.org"
PORT = 13377

def decode_data(data):
    t = data["type"]
    e = data["encoded"]

    if t == "base64":
        return base64.b64decode(e).decode()

    elif t == "hex":
        return bytes.fromhex(e).decode()

    elif t == "rot13":
        return codecs.decode(e, "rot_13")

    elif t == "bigint":
        n = int(e, 16)  
        b = n.to_bytes((n.bit_length() + 7) // 8, "big")
        return b.decode()

    elif t == "utf-8":
        return "".join(chr(x) for x in e)

    else:
        raise ValueError(f"Unknown type: {t}")

with socket.create_connection((HOST, PORT)) as s:
    f = s.makefile("rw")

    while True:
        line = f.readline()
        if not line:
            break

        data = json.loads(line)
        print("Received:", data)

        if "flag" in data:
            print("FLAG:", data["flag"])
            break

        decoded = decode_data(data)
        response = {"decoded": decoded}

        f.write(json.dumps(response) + "\n")
        f.flush()
