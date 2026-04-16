import hashlib


def manual_sha1(message):
    steps = []

    def left_rotate(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    # Pre-processing (Padding)
    message_bytes = bytearray(message, 'utf-8')
    original_len_bytes = len(message_bytes)
    orig_len_in_bits = (8 * original_len_bytes) & 0xFFFFFFFFFFFFFFFF

    steps.append(f"Input message: {message}")
    steps.append(f"Input bytes length: {original_len_bytes}")
    steps.append(f"Input bits length: {orig_len_in_bits}")
    steps.append("")

    message_bytes.append(0x80)
    steps.append("After appending 0x80:")
    steps.append(message_bytes.hex())

    while (len(message_bytes) * 8) % 512 != 448:
        message_bytes.append(0)

    steps.append("After zero padding to 448 mod 512:")
    steps.append(f"Total bytes before length append: {len(message_bytes)}")

    message_bytes += orig_len_in_bits.to_bytes(8, 'big')
    steps.append("After appending original length (64-bit big-endian):")
    steps.append(message_bytes.hex())
    steps.append(f"Final padded length in bytes: {len(message_bytes)}")
    steps.append(f"Total chunks: {len(message_bytes) // 64}")
    steps.append("")

    # Initial Variables
    h0, h1, h2, h3, h4 = (
        0x67452301,
        0xEFCDAB89,
        0x98BADCFE,
        0x10325476,
        0xC3D2E1F0,
    )

    steps.append("Initial hash values:")
    steps.append(f"h0={h0:08x}, h1={h1:08x}, h2={h2:08x}, h3={h3:08x}, h4={h4:08x}")
    steps.append("")

    # Process 512-bit chunks
    for chunk_index, chunk_start in enumerate(range(0, len(message_bytes), 64), start=1):
        chunk = message_bytes[chunk_start:chunk_start + 64]

        steps.append(f"=== Chunk {chunk_index} ===")
        steps.append(f"Chunk hex: {chunk.hex()}")

        w = [0] * 80
        for i in range(16):
            w[i] = int.from_bytes(chunk[i * 4:i * 4 + 4], 'big')

        for i in range(16, 80):
            w[i] = left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

        steps.append("First 16 words (w[0..15]):")
        for i in range(16):
            steps.append(f"w[{i:02}] = {w[i]:08x}")
        steps.append("")

        a, b, c, d, e = h0, h1, h2, h3, h4

        # 80 rounds
        for i in range(80):
            if 0 <= i <= 19:
                f, k = (b & c) | ((~b) & d), 0x5A827999
            elif 20 <= i <= 39:
                f, k = b ^ c ^ d, 0x6ED9EBA1
            elif 40 <= i <= 59:
                f, k = (b & c) | (b & d) | (c & d), 0x8F1BBCDC
            else:
                f, k = b ^ c ^ d, 0xCA62C1D6

            temp = (left_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF
            e, d, c, b, a = d, c, left_rotate(b, 30), a, temp

            # Intermediate result snapshots (full cycle checkpoints)
            if i in (0, 19, 39, 59, 79):
                steps.append(
                    f"Round {i:02}: a={a:08x} b={b:08x} c={c:08x} d={d:08x} e={e:08x}"
                )

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

        steps.append("Updated hash after chunk:")
        steps.append(f"h0={h0:08x}, h1={h1:08x}, h2={h2:08x}, h3={h3:08x}, h4={h4:08x}")
        steps.append("")

    result = '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

    # Verification check
    verify = hashlib.sha1(message.encode()).hexdigest()
    steps.append(f"Final SHA-1 Hash: {result}")
    steps.append(f"Verified (hashlib): {verify}")
    steps.append(f"Match: {'YES' if result == verify else 'NO'}")

    return result, verify, steps
