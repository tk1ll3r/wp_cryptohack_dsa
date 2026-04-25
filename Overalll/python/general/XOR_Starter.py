label = "label"
result = "".join(chr(ord(c) ^ 13) for c in label)
print(f"crypto{{{result}}}")
