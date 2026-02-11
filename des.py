# -------- STATIC VALUES --------

P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8  = [6, 3, 7, 4, 8, 5, 10, 9]
P4  = [2, 4, 3, 1]

IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]

S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]


def bits_str(arr):
    return ''.join(str(b) for b in arr)


# -------- KEY GENERATION --------
def generatekey(key):
    steps = []
    steps.append(f"Plaintext: {key}")
    steps.append(f"Key: {key}")

    p10_key = [int(key[i-1]) for i in P10]
    steps.append(f"P10: {P10}")
    steps.append(f"After P10: {bits_str(p10_key)}")

    left, right = p10_key[:5], p10_key[5:]
    steps.append(f"Split → Left: {bits_str(left)}  Right: {bits_str(right)}")

    # LS-1
    ls1_left = left[1:] + left[:1]
    ls1_right = right[1:] + right[:1]
    ls1 = ls1_left + ls1_right
    steps.append(f"LS-1: {bits_str(ls1_left)}  {bits_str(ls1_right)}")

    k1 = [ls1[i-1] for i in P8]
    steps.append(f"P8: {P8}")
    steps.append(f"K1: {bits_str(k1)}")

    # LS-2
    ls2_left = ls1_left[2:] + ls1_left[:2]
    ls2_right = ls1_right[2:] + ls1_right[:2]
    ls2 = ls2_left + ls2_right
    steps.append(f"LS-2: {bits_str(ls2_left)}  {bits_str(ls2_right)}")

    k2 = [ls2[i-1] for i in P8]
    steps.append(f"K2: {bits_str(k2)}")

    return k1, k2, steps


# -------- ROUND FUNCTION --------
def fk(bits, subkey, round_name, steps):
    left, right = bits[:4], bits[4:]
    steps.append(f"--- {round_name} ---")
    steps.append(f"Input: {bits_str(bits)}")
    steps.append(f"Left: {bits_str(left)}   Right: {bits_str(right)}")

    ep = [right[i-1] for i in EP]
    steps.append(f"EP: {EP}")
    steps.append(f"After EP: {bits_str(ep)}")

    xor = [a ^ b for a, b in zip(ep, subkey)]
    steps.append(f"Key: {bits_str(subkey)}")
    steps.append(f"EP XOR Key: {bits_str(xor)}")

    left_xor = xor[:4]
    right_xor = xor[4:]

    row1 = left_xor[0]*2 + left_xor[3]
    col1 = left_xor[1]*2 + left_xor[2]
    row2 = right_xor[0]*2 + right_xor[3]
    col2 = right_xor[1]*2 + right_xor[2]

    steps.append(f"S0 → row={row1}, col={col1}")
    steps.append(f"S1 → row={row2}, col={col2}")

    s0_val = S0[row1][col1]
    s1_val = S1[row2][col2]
    steps.append(f"S0 value: {s0_val}  →  {format(s0_val, '02b')}")
    steps.append(f"S1 value: {s1_val}  →  {format(s1_val, '02b')}")

    s_bits = [int(b) for b in format(s0_val, '02b')] + \
             [int(b) for b in format(s1_val, '02b')]
    steps.append(f"S-box output: {bits_str(s_bits)}")

    p4 = [s_bits[i-1] for i in P4]
    steps.append(f"P4: {P4}")
    steps.append(f"After P4: {bits_str(p4)}")

    left_result = [l ^ p for l, p in zip(left, p4)]
    steps.append(f"Left XOR P4: {bits_str(left_result)}")

    result = left_result + right
    steps.append(f"Result: {bits_str(result)}")
    return result


# -------- ENCRYPTION --------
def des_encrypt(plaintext, key):
    steps = []
    steps.append(f"Plaintext: {plaintext}")
    steps.append(f"Key: {key}")
    steps.append("")

    # Key generation
    steps.append("=== KEY GENERATION ===")
    k1, k2, key_steps = generatekey(key)
    steps.extend(key_steps)
    steps.append("")

    # Initial Permutation
    steps.append("=== ENCRYPTION ===")
    ip = [int(plaintext[i-1]) for i in IP]
    steps.append(f"IP: {IP}")
    steps.append(f"After IP: {bits_str(ip)}")
    steps.append("")

    # Round 1
    round1 = fk(ip, k1, "Complex Function 1 (with K1)", steps)
    steps.append("")

    # Swap
    swapped = round1[4:] + round1[:4]
    steps.append(f"After Swap: {bits_str(swapped)}")
    steps.append("")

    # Round 2
    round2 = fk(swapped, k2, "Complex Function 2 (with K2)", steps)
    steps.append("")

    # Inverse IP
    cipher = [round2[i-1] for i in IP_inv]
    steps.append(f"IP⁻¹: {IP_inv}")
    steps.append(f"Ciphertext: {bits_str(cipher)}")

    return bits_str(cipher), steps
