def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modinv(a, m=26):
    for i in range(m):
        if (a * i) % m == 1:
            return i

def affine_encrypt(text, a, b):
    text = text.upper()
    res = ""
    for ch in text:
        if ch.isalpha():
            x = ord(ch) - 65
            res += chr((a * x + b) % 26 + 65)
        else:
            res += ch
    return res

def affine_decrypt(text, a, b):
    inv = modinv(a)
    res = ""
    for ch in text:
        if ch.isalpha():
            y = ord(ch) - 65
            res += chr((inv * (y - b)) % 26 + 65)
        else:
            res += ch
    return res
