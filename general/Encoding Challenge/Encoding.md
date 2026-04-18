> ### 5. Encoding Challenge

> Given

- Đây là một bài **interactive challenge**.
- Server sẽ gửi về dữ liệu ở dạng JSON, gồm:
  - `type`: kiểu mã hóa
  - `encoded`: dữ liệu đã mã hóa
- Nhiệm vụ của mình là giải mã giá trị `encoded` theo đúng kiểu `type`, rồi gửi lại cho server đúng dạng.

> Goal 

- Kết nối tới server của challenge
- Nhận dữ liệu mã hóa mà server gửi về
- Xác định kiểu mã hóa qua trường type
- Giải mã trường encoded về chuỗi gốc
- Gửi lại đáp án đúng cho server dưới dạng JSON
- Lặp lại nhiều lần cho đến khi server trả về flag

> Solution

```python
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
```

Chạy code ra được flag `crypto{3nc0d3_d3c0d3_3nc0d3}`
<img width="964" height="261" alt="image" src="https://github.com/user-attachments/assets/ef86d54e-20bf-4631-ba3d-3292900c0470" />


---
