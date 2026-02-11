# -------- AES S-Box --------
sbox = [
    ['63','7C','77','7B','F2','6B','6F','C5','30','01','67','2B','FE','D7','AB','76'],
    ['CA','82','C9','7D','FA','59','47','F0','AD','D4','A2','AF','9C','A4','72','C0'],
    ['B7','FD','93','26','36','3F','F7','CC','34','A5','E5','F1','71','D8','31','15'],
    ['04','C7','23','C3','18','96','05','9A','07','12','80','E2','EB','27','B2','75'],
    ['09','83','2C','1A','1B','6E','5A','A0','52','3B','D6','B3','29','E3','2F','84'],
    ['53','D1','00','ED','20','FC','B1','5B','6A','CB','BE','39','4A','4C','58','CF'],
    ['D0','EF','AA','FB','43','4D','33','85','45','F9','02','7F','50','3C','9F','A8'],
    ['51','A3','40','8F','92','9D','38','F5','BC','B6','DA','21','10','FF','F3','D2'],
    ['CD','0C','13','EC','5F','97','44','17','C4','A7','7E','3D','64','5D','19','73'],
    ['60','81','4F','DC','22','2A','90','88','46','EE','B8','14','DE','5E','0B','DB'],
    ['E0','32','3A','0A','49','06','24','5C','C2','D3','AC','62','91','95','E4','79'],
    ['E7','C8','37','6D','8D','D5','4E','A9','6C','56','F4','EA','65','7A','AE','08'],
    ['BA','78','25','2E','1C','A6','B4','C6','E8','DD','74','1F','4B','BD','8B','8A'],
    ['70','3E','B5','66','48','03','F6','0E','61','35','57','B9','86','C1','1D','9E'],
    ['E1','F8','98','11','69','D9','8E','94','9B','1E','87','E9','CE','55','28','DF'],
    ['8C','A1','89','0D','BF','E6','42','68','41','99','2D','0F','B0','54','BB','16']
]

# -------- Final Round Key (static) --------
round_key = [
    ['A1','B2','C3','D4'],
    ['E5','F6','07','18'],
    ['29','3A','4B','5C'],
    ['6D','7E','8F','90']
]


def fmt_matrix(matrix):
    """Format a 4x4 matrix as lines of text."""
    lines = []
    for row in matrix:
        lines.append('  '.join(row))
    return lines


def mul2(x):
    x = int(x, 16)
    res = x << 1
    if res & 0x100:
        res = (res & 0xFF) ^ 0x1B
    return res & 0xFF


def mul3(x):
    return mul2(x) ^ int(x, 16)


def aes_encrypt(pt, key, rounds):
    """
    pt  : 4x4 list of hex strings  e.g. [['0A','1B',...], ...]
    key : 4x4 list of hex strings
    rounds : int
    Returns (final_state, steps)
    """
    steps = []

    steps.append("Plaintext Matrix:")
    steps.extend(fmt_matrix(pt))
    steps.append("")
    steps.append("Key Matrix:")
    steps.extend(fmt_matrix(key))
    steps.append("")

    state = pt

    for rnd in range(1, rounds + 1):
        steps.append(f"{'='*40}")
        steps.append(f"ROUND {rnd}")
        steps.append(f"{'='*40}")
        steps.append("")

        # --- AddRoundKey (XOR with key) ---
        xor_matrix = []
        for i in range(4):
            row = []
            for j in range(4):
                xor_val = int(state[i][j], 16) ^ int(key[i][j], 16)
                row.append(format(xor_val, '02X'))
            xor_matrix.append(row)

        steps.append("XOR Result Matrix:")
        steps.extend(fmt_matrix(xor_matrix))
        steps.append("")

        # --- SubBytes ---
        sub_matrix = []
        for i in range(4):
            row = []
            for j in range(4):
                byte = xor_matrix[i][j]
                r = int(byte[0], 16)
                c = int(byte[1], 16)
                row.append(sbox[r][c])
            sub_matrix.append(row)

        steps.append("SubBytes Result Matrix:")
        steps.extend(fmt_matrix(sub_matrix))
        steps.append("")

        # --- ShiftRows ---
        shifted_matrix = []
        for i in range(4):
            row = sub_matrix[i]
            shifted_row = row[i:] + row[:i]
            shifted_matrix.append(shifted_row)

        steps.append("ShiftRows Result Matrix:")
        steps.extend(fmt_matrix(shifted_matrix))
        steps.append("")

        # --- MixColumns ---
        mix_result = [['' for _ in range(4)] for _ in range(4)]

        for c in range(4):
            s0 = shifted_matrix[0][c]
            s1 = shifted_matrix[1][c]
            s2 = shifted_matrix[2][c]
            s3 = shifted_matrix[3][c]

            r0 = mul2(s0) ^ mul3(s1) ^ int(s2, 16) ^ int(s3, 16)
            r1 = int(s0, 16) ^ mul2(s1) ^ mul3(s2) ^ int(s3, 16)
            r2 = int(s0, 16) ^ int(s1, 16) ^ mul2(s2) ^ mul3(s3)
            r3 = mul3(s0) ^ int(s1, 16) ^ int(s2, 16) ^ mul2(s3)

            mix_result[0][c] = format(r0 & 0xFF, '02X')
            mix_result[1][c] = format(r1 & 0xFF, '02X')
            mix_result[2][c] = format(r2 & 0xFF, '02X')
            mix_result[3][c] = format(r3 & 0xFF, '02X')

        steps.append("MixColumns Result Matrix:")
        steps.extend(fmt_matrix(mix_result))
        steps.append("")

        # --- AddRoundKey (with round_key) ---
        final_matrix = []
        for i in range(4):
            row = []
            for j in range(4):
                val = int(mix_result[i][j], 16) ^ int(round_key[i][j], 16)
                row.append(format(val, '02X'))
            final_matrix.append(row)

        steps.append("Final Matrix After AddRoundKey:")
        steps.extend(fmt_matrix(final_matrix))
        steps.append("")

        state = final_matrix

    steps.append(f"{'='*40}")
    steps.append("FINAL CIPHERTEXT:")
    steps.extend(fmt_matrix(state))

    return state, steps
