KEY1     = bytes.fromhex("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313")
K2xK1    = bytes.fromhex("37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e")
K2xK3    = bytes.fromhex("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1")
FxK1xK3xK2 = bytes.fromhex("04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf")

KEY2 = bytes(a ^ b for a, b in zip(K2xK1, KEY1))
KEY3 = bytes(a ^ b for a, b in zip(K2xK3, KEY2))
FLAG = bytes(a ^ b ^ c ^ d for a, b, c, d in zip(FxK1xK3xK2, KEY1, KEY3, KEY2))

print(FLAG.decode())