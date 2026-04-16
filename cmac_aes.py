from Crypto.Cipher import AES

BLOCK_SIZE = 16


def str_to_bytes(s):
    return bytes([ord(c) for c in s])


def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


def left_shift(b):
    return ((int.from_bytes(b, 'big') << 1) & (2**128 - 1)).to_bytes(16, 'big')


def generate_subkeys(key):
    cipher = AES.new(key, AES.MODE_ECB)
    L = cipher.encrypt(b'\x00' * 16)

    Rb = b'\x00' * 15 + b'\x87'

    K1 = left_shift(L)
    if L[0] & 0x80:
        K1 = xor_bytes(K1, Rb)

    K2 = left_shift(K1)
    if K1[0] & 0x80:
        K2 = xor_bytes(K2, Rb)

    return L, K1, K2


def cmac_step_by_step(key_str, msg_str):
    steps = []

    steps.append(f"Original Key: {key_str}")
    steps.append(f"Message: {msg_str}")

    key = str_to_bytes(key_str)
    msg = str_to_bytes(msg_str)

    steps.append("")
    steps.append(f"[1] Key (bytes): {key}")
    steps.append(f"[2] Message (bytes): {msg}")

    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes after manual encoding.")

    L, K1, K2 = generate_subkeys(key)
    steps.append("")
    steps.append(f"[3] L = AES_K(0^128): {L.hex()}")
    steps.append(f"[4] K1: {K1.hex()}")
    steps.append(f"[5] K2: {K2.hex()}")

    # Message block split
    n = len(msg)
    if n == 0:
        n_blocks = 1
    else:
        n_blocks = (n + BLOCK_SIZE - 1) // BLOCK_SIZE

    blocks = []
    for i in range(n_blocks - 1):
        blocks.append(msg[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE])

    last_block_start = (n_blocks - 1) * BLOCK_SIZE
    last = msg[last_block_start:last_block_start + BLOCK_SIZE]

    is_complete = len(last) == BLOCK_SIZE and n != 0

    if is_complete:
        M_last = xor_bytes(last, K1)
        steps.append("")
        steps.append("[6] Last block is complete -> M_last = last_block XOR K1")
        steps.append(f"    last_block: {last.hex()}")
        steps.append(f"    M_last: {M_last.hex()}")
    else:
        pad_len = BLOCK_SIZE - len(last)
        padded_last = last + b'\x80' + b'\x00' * (pad_len - 1)
        M_last = xor_bytes(padded_last, K2)
        steps.append("")
        steps.append("[6] Last block is incomplete/empty -> pad then XOR with K2")
        steps.append(f"    last_block: {last.hex()}")
        steps.append(f"    padded_last: {padded_last.hex()}")
        steps.append(f"    M_last: {M_last.hex()}")

    cipher = AES.new(key, AES.MODE_ECB)
    X = b'\x00' * BLOCK_SIZE
    steps.append("")
    steps.append(f"[7] Initial X: {X.hex()}")

    for idx, block in enumerate(blocks, start=1):
        Y = xor_bytes(X, block)
        X = cipher.encrypt(Y)
        steps.append(f"[8.{idx}] Block {idx}: {block.hex()}")
        steps.append(f"      Y = X XOR block: {Y.hex()}")
        steps.append(f"      X = AES_K(Y): {X.hex()}")

    Y = xor_bytes(X, M_last)
    T = cipher.encrypt(Y)

    steps.append("")
    steps.append(f"[9] Y = X XOR M_last: {Y.hex()}")
    steps.append(f"[10] CMAC Tag = AES_K(Y): {T.hex()}")

    return T.hex(), steps
