def construct_matrix(string, n):
    matrix = list()
    index = 0
    st_char = 97
    s_str = set(string)
    list2 = list(dict.fromkeys(string))
    n_1 = len(s_str)
    
    for i in range(5):
        row = []
        for j in range(5):
            if index < n_1:
                row.append(list2[index])
                index = index + 1
            else:
                while True:
                    ch = chr(st_char)
                    exists = any(ch in sublist for sublist in matrix)
                    if exists or ch in row:
                        st_char = st_char + 1
                    else:
                        row.append(ch)
                        st_char = st_char + 1
                        break
        matrix.append(row)
    
    return matrix


def find(ch1, ch2, matrix):
    d = dict()
    d[ch1] = []
    d[ch2] = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == ch1 or matrix[i][j] == ch2:
                d[matrix[i][j]].append([i, j])
    return d


def encrypt(string, n, matrix):
    stack = []
    l = list()
    verbose = 'x'
    char_count = 0
    
    for i in string:
        stack.append(i)
        if len(stack) == 2:
            e2 = stack.pop()
            e1 = stack.pop()
            if e1 == e2:
                if e1 == verbose:
                    l.append([e1, 'q'])
                    char_count += 1
                else:
                    stack.append(e1)
                    l.append([e1, verbose])
                    char_count += 1
            else:
                l.append([e1, e2])
                char_count += 2
    
    if char_count != n:
        l.append([string[-1], verbose])
    
    en_input = ""
    for x, y in l:
        d = find(x, y, matrix)
        l1 = d.values()
        lists = [x for v in d.values() for x in v[0]]
        
        if lists[0] == lists[2]:
            ch = matrix[(lists[0] + 1) % len(matrix)][lists[1]]
            ch2 = matrix[(lists[2] + 1) % len(matrix)][lists[3]]
            en_input = en_input + ch2 + ch
        elif lists[1] == lists[3]:
            ch = matrix[lists[0]][(lists[1] + 1) % 5]
            ch2 = matrix[lists[2]][(lists[3] + 1) % 5]
            en_input = en_input + ch2 + ch
        else:
            ch = matrix[lists[0]][lists[3]]
            ch2 = matrix[lists[2]][lists[1]]
            en_input = en_input + ch + ch2
    
    return en_input


def decrypt(string, n, matrix):
    stack = []
    l = list()
    verbose = 'x'
    char_count = 0
    
    for i in string:
        stack.append(i)
        if len(stack) == 2:
            e2 = stack.pop()
            e1 = stack.pop()
            if e1 == e2:
                if e1 == verbose:
                    l.append([e1, 'q'])
                    char_count += 1
                else:
                    stack.append(e1)
                    l.append([e1, verbose])
                    char_count += 1
            else:
                l.append([e1, e2])
                char_count += 2
    
    if char_count != n:
        l.append([string[-1], verbose])
    
    de_input = ""
    for x, y in l:
        d = find(x, y, matrix)
        l1 = d.values()
        lists = [x for v in d.values() for x in v[0]]
        
        if lists[0] == lists[2]:
            ch = matrix[(lists[0] - 1 + 5) % len(matrix)][lists[1]]
            ch2 = matrix[(lists[2] - 1 + 5) % len(matrix)][lists[3]]
            de_input = de_input + ch2 + ch
        elif lists[1] == lists[3]:
            ch = matrix[lists[0]][(lists[1] - 1 + 5) % 5]
            ch2 = matrix[lists[2]][(lists[3] - 1 + 5) % 5]
            de_input = de_input + ch2 + ch
        else:
            ch = matrix[lists[0]][lists[3]]
            ch2 = matrix[lists[2]][lists[1]]
            de_input = de_input + ch + ch2
    
    if n > 2 or n == 1:
        decryption = de_input[:-1]
    else:
        decryption = de_input
    
    return decryption


# Flask interface functions
def playfair_encrypt(text, key):
    # Clean the input
    text = text.lower().replace(" ", "")
    key = key.lower().replace(" ", "")
    
    # Construct matrix with the key
    matrix = construct_matrix(key, len(key))
 
    result = encrypt(text, len(text), matrix)
    
    return result.upper()


def playfair_decrypt(text, key):
    # Clean the input
    text = text.lower().replace(" ", "")
    key = key.lower().replace(" ", "")
    
    # Construct matrix with the key
    matrix = construct_matrix(key, len(key))
    
    # Decrypt using the custom logic
    result = decrypt(text, len(text), matrix)
    
    return result.upper()


def get_key_matrix(key):
    # Clean the key
    key = key.lower().replace(" ", "")
    return construct_matrix(key, len(key))