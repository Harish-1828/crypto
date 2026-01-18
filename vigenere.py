def gen_key(text, key):
    key = list(key)
    for i in range(len(text) - len(key)):
        key.append(key[i])
    return "".join(key)

def vigenere_encrypt(text, key):
    text = text.upper()
    key = gen_key(text, key)
    res = ""
    for t, k in zip(text, key):
        if t.isalpha():
            res += chr(((ord(t)-65)+(ord(k)-65))%26+65)
        else:
            res += t
    return res

def vigenere_decrypt(text, key):
    text = text.upper()
    key = gen_key(text, key)
    res = ""
    for t, k in zip(text, key):
        if t.isalpha():
            res += chr(((ord(t)-65)-(ord(k)-65)+26)%26+65)
        else:
            res += t
    return res
