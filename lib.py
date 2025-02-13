# encode=lambda s: "".join(map(lambda x:chr([0xE0100 + (x - 16), 0xFE00 + x][x < 16]), map(ord, s)))
# decode=lambda s: "".join(map(lambda x: chr(x - (0xFE00 if x in range(0xFE00, 0xFE0F+1) else 0xE0100) + [0, 16][x in range(0xE0100, 0xE01EF+1)]), map(ord, s)))

from itertools import zip_longest


def encode_char(x):
    x = ord(x)
    if x < 16:
        return chr(x + 0xFE00)
    return chr(0xE0100 + (x - 16))

def decode_char(x):
    x = ord(x)
    if x in range(0xFE00, 0XFE0F+1):
        return chr(x - 0xFE00)
    elif x in range(0xE0100, 0xE01EF+1):
        return chr(x - 0xE0100 + 16)
    else:
        return ""

def encode(s):
    return "".join(map(encode_char, s))

def encode_hidden(s, S):
    return ''.join(map(''.join, zip_longest(S, encode(s), fillvalue="")))

def decode(s):
    return "".join(map(decode_char, s))


# normal = "this is incredibly stupid"
# print((encoded := encode("hidden message :3", normal)))
# print(decode(encoded))
