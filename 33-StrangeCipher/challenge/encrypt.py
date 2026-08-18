def xor_encrypt(text, key):
    res = []
    for i in range(len(text)):
        res.append(chr(ord(text[i]) ^ ord(key[i % len(key)])))
    return "".join(res)

if __name__ == "__main__":
    # flag = "..."
    # key = "secret_key"
    # encrypted = xor_encrypt(flag, key)
    # print(encrypted)
    pass
