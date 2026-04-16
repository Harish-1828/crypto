import hashlib


def str_to_bytes(s):
    return bytes([ord(c) for c in s])  # manual encoding


def hmac_step_by_step(key, message):
    BLOCK_SIZE = 64
    steps = []

    steps.append(f"Original Key: {key}")
    steps.append(f"Message: {message}")

    key = str_to_bytes(key)
    message = str_to_bytes(message)

    steps.append("")
    steps.append(f"[1] Key (bytes): {key}")
    steps.append(f"[2] Message (bytes): {message}")

    # Step 1: Key padding
    if len(key) < BLOCK_SIZE:
        key = key + b'\x00' * (BLOCK_SIZE - len(key))

    steps.append("")
    steps.append(f"[3] Padded Key (64 bytes): {key}")

    # Step 2: ipad & opad
    ipad = bytes([0x36] * BLOCK_SIZE)
    opad = bytes([0x5C] * BLOCK_SIZE)

    steps.append("")
    steps.append(f"[4] ipad: {ipad}")
    steps.append(f"[5] opad: {opad}")

    # Step 3: XOR
    k_ipad = bytes([k ^ i for k, i in zip(key, ipad)])
    k_opad = bytes([k ^ o for k, o in zip(key, opad)])

    steps.append("")
    steps.append(f"[6] Key ⊕ ipad: {k_ipad}")
    steps.append(f"[7] Key ⊕ opad: {k_opad}")

    # Step 4: Inner hash
    inner_data = k_ipad + message
    steps.append("")
    steps.append(f"[8] Inner Input (k_ipad + message): {inner_data}")

    inner_hash = hashlib.sha1(inner_data).digest()
    steps.append(f"[9] Inner Hash: {inner_hash}")

    # Step 5: Outer hash
    outer_data = k_opad + inner_hash
    steps.append("")
    steps.append(f"[10] Outer Input (k_opad + inner_hash): {outer_data}")

    final_hash = hashlib.sha1(outer_data).hexdigest()
    steps.append(f"[11] Final HMAC: {final_hash}")

    return final_hash, steps
