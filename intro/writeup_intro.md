### Introduction
---
> #### 2. Great Snakes
Đây là bài làm quen với việc cho file .py hoạt động
Chúng ta có được file `great_snakes.py` với nội dung:
```python
#!/usr/bin/env python3

import sys
# import this

if sys.version_info.major == 2:
    print("You are running Python 2, which is no longer supported. Please update to Python 3.")

ords = [81, 64, 75, 66, 70, 93, 73, 72, 1, 92, 109, 2, 84, 109, 66, 75, 70, 90, 2, 92, 79]

print("Here is your flag:")
print("".join(chr(o ^ 0x32) for o in ords))

```
 #####  Chạy file với py3 ta được flag:
`crypto{z3n_0f_pyth0n}`

![Ảnh chạy file](intro.png)

---
