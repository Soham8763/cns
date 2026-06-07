# RSA
def encryption(m):
    p = 7
    q = 11
    n = p*q
    phi = (p-1)*(q-1)
    e = 7
    print("Public Key",(e,n))
    d = 1
    while (d*3)%phi != 1:
        d+=1
    print("Private Key",(d,n))
    encrypt = (m**e)%n
    print(encrypt)
    decrypt = (encrypt**d)%n
    print(decrypt)

# PLayfair Cipher
def generate_matrix(keyword):
    keyword = keyword.upper().replace("J","I")
    matrix = []
    used = set()
    for ch in keyword and ch not in used:
        matrix.append(ch)
        used.add(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in used:
            matrix.append(ch)
    return [matrix[i:i+5] for i in range(0,25,5)]

def find_position(ch,matrix):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i,j

def prepare_text(text):
    text = text.upper().replace("J","I")
    result += "".join(ch for ch in text if ch.isalpha()) # Remove spaces and special characters
    i = 0
    while i<len(text):
        a = text[i]
        if i+1 < len(text):
            b = text[i+1]
            if a == b:
                result += a+"X"
                i+=1
            else:
                result = a+b
                i+=2
        else:
            result += a+"X"
            i+=1
    return result

def encrypt(text,keyword):
    matrix = generate_matrix(keyword)
    text = prepare_text(text)
    cipher = ""
    for i in range(0,len(text),2):
        a,b = text[i],text[i+1]
        r1,c1 = find_position(a,matrix)
        r2,c2 = find_position(b,matrix)

        if r1 == r2:
            cipher += matrix[r1][(c1+1)%5]
            cipher += matrix[r2][(c2+1)%5]
        elif c1 == c2:
            cipher += matrix[(r1+1)%5][c1]
            cipher += matrix[(r2+1)%5][c2]
        else:
            cipher += matrix[r1][c2]
            cipher += matrix[r2][c1]

    return cipher

# Vignere Cipher
def encrypt_vignere(text,key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    text = text.upper()
    key = key.upper()
    key_index = 0
    result = ""
    for ch in text:
        if ch in alphabet:
            text_position = alphabet.index(ch)
            key_char = key[key_index%len(key)]
            key_pos = alphabet.index(key_char)

            new_pos = text_position+key_pos
            if new_pos >= 26:
                new_pos-=26

            result+=alphabet[new_pos]
            key_index+=1
        else:
            result+=ch
    return result

# Deffie-Hellman
def deffie_hellman():
    p = int(input("Enter prime number (p): "))
    g = int(input("Enter primitive root (g): "))

    a = int(input("Enter Alice private key: "))
    b = int(input("Enter Bob private key: "))

    A = pow(g,a,p)
    B = pow(g,b,p)

    K1 = pow(B,a,p)
    K2 = pow(A,b,p)

    print("Alice Public Key =", A)
    print("Bob Public Key =", B)

    print("Shared Secret Key (Alice) =", key1)
    print("Shared Secret Key (Bob) =", key2)

deffie_hellman()

# DES
# Generate the 16 round keys
def hex_to_bin(hex_text):
    binary = bin(int(hex_text, 16))[2:].zfill(len(hex_text)*4)
    return binary

def bin_to_hex(bin_text):
    hex = hex(int(bin_text, 2))[2:].upper()
    return hex

def permute(text,table):
    result = ""
    for i in table:
        result += text[i-1]
    return result

def shift_left(text,n):
    return text[n:]+text[:m]

def generate_round_keys(key_64bit):
    round_keys = []
    key_56bit = permute(key_64bit,PC_1)
    left = key_56bit[:28]
    right = key_56bit[28:]
    for i in range(16):
        left = shift_left(left,shift_table[i])
        right = shift_left(right,shift_table[i])
        merged = left+right
        round_key = permute(merged,PC_2)
        round_keys.append(round_key)

    return round_keys

# Encryption and Decryption
def xor(a,b):
    result = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            result += "0"
        else:
            result += "1"

    return result

def sbox_substition(data):
    result = ""
    for i in range(8):
        block = data[i*6:(i+1)*6]
        row = int(block[0] + block[5],2)
        col = int(block[1:5],2)
        value = S_BOX[i][row][col]
        result += format(value,"04b")

    return result

def des_function(right,round_key):
    expanded_right = permute(right,E_TABLE)
    xor_result = xor(expanded_right,round_key)
    sbox_result = sbox_substition(xor_result)
    final_result = permute(sbox_result,P_BOX)

    return final_result

def des_encryption(plaintext,round_keys):
    plaintext = permute(plaintext,IP)
    left = plaintext[:32]
    right = plaintext[32:]

    for i in range(16):
        temp = right
        function_result = des_function(right,round_keys[i])
        right = xor(function_result,left)
        left = temp

    combined = left+right
    cipher_text = permute(combined,FP)

    return cipher_text

def des_decryption(ciphertext, round_keys):
    reversed_keys = round_keys[::-1]

    plaintext = des_encrypt(
        ciphertext,
        reversed_keys
    )

    return plaintext

# MAIN DRIVER
plaintext_hex = input(
    "Enter Plaintext (16 hex digits): "
)

key_hex = input(
    "Enter Key (16 hex digits): "
)

plaintext_bin = hex_to_bin(
    plaintext_hex
)

key_bin = hex_to_bin(
    key_hex
)

round_keys = generate_round_keys(
    key_bin
)

ciphertext_bin = des_encrypt(
    plaintext_bin,
    round_keys
)

ciphertext_hex = bin_to_hex(
    ciphertext_bin
)

print("Ciphertext:", ciphertext_hex)