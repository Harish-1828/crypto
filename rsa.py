import math


def is_prime_check(n):
    """Simple primality check."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def rsa_encrypt_decrypt(p, q, m):
    """
    RSA encryption and decryption.
    Returns (result_dict, steps)
    """
    steps = []

    # Prime check
    steps.append(f"p = {p}")
    if is_prime_check(p):
        steps.append(f"{p} is Prime ✓")
    else:
        steps.append(f"{p} is NOT Prime ✗")
        return None, steps

    steps.append("")
    steps.append(f"q = {q}")
    if is_prime_check(q):
        steps.append(f"{q} is Prime ✓")
    else:
        steps.append(f"{q} is NOT Prime ✗")
        return None, steps

    steps.append("")

    # n = p * q
    n = p * q
    steps.append(f"n = p × q = {p} × {q} = {n}")

    # phi(n)
    phi = (p - 1) * (q - 1)
    steps.append(f"φ(n) = (p-1)(q-1) = ({p}-1)({q}-1) = {phi}")
    steps.append("")

    # choose e
    e = 3
    while math.gcd(e, phi) != 1:
        e += 2
    steps.append(f"Choose e such that gcd(e, φ(n)) = 1")
    steps.append(f"e = {e}")
    steps.append(f"gcd({e}, {phi}) = {math.gcd(e, phi)} ✓")
    steps.append("")

    # compute d
    d = pow(e, -1, phi)
    steps.append(f"d = e⁻¹ mod φ(n)")
    steps.append(f"d = {e}⁻¹ mod {phi} = {d}")
    steps.append("")

    steps.append(f"Public Key  (e, n) = ({e}, {n})")
    steps.append(f"Private Key (d, n) = ({d}, {n})")
    steps.append("")

    # encryption
    cipher = pow(m, e, n)
    steps.append(f"Encryption: C = M^e mod n")
    steps.append(f"C = {m}^{e} mod {n} = {cipher}")
    steps.append("")

    # decryption
    plain = pow(cipher, d, n)
    steps.append(f"Decryption: M = C^d mod n")
    steps.append(f"M = {cipher}^{d} mod {n} = {plain}")
    steps.append("")

    steps.append(f"Encrypted: {cipher}")
    steps.append(f"Decrypted: {plain}")

    result = {
        "e": e,
        "n": n,
        "d": d,
        "cipher": cipher,
        "plain": plain
    }

    return result, steps
