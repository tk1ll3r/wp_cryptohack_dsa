bytes2long = lambda x: int.from_bytes(x, 'big')

x = mod(bytes2long(b"VOTE FOR PEDRO"), 2**120).nth_root(3)

print('{' + f'"option":"vote","vote":"{hex(x)[2:]}"' + '}')
