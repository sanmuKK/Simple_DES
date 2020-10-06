from table import ip, ip_, pc1, pc2, table_e, table_p, s_box


def change_hex_to_bin(s):
    a = bin(int(s, 16))[2:].upper().rjust(64, '0')
    return a


def xor(left, right):
    result = int(left, 2) ^ int(right, 2)
    return bin(result)[2:].rjust(len(left), '0')


def translation(s, list_1):
    result = ''
    for i in list_1:
        result += s[i-1]
    return result


def move(lst, k):
    k *= -1
    len2 = len(lst)
    ss = (lst[k:]+lst[:k]).rjust(len2, '0')
    return str(ss)


def func_f(right, key):
    result = translation(right, table_e)
    result = xor(str(result), str(key))
    result2 = ''
    for i in range(0, len(result)-5, 6):
        j = i // 6
        r = int(result[i] + result[i + 5], 2)
        n = int(result[i + 1] + result[i + 2] + result[i + 3] + result[i + 4], 2)
        d = s_box[j][r * 16 + n]
        result2 += bin(d)[2:].upper().rjust(4, '0')
    result = translation(result2, table_p)
    return str(result)


def generate_secret(key, r):
    current_key_bin = bin(int(str(key), 16))[2:].rjust(64, '0')
    current_key_bin = translation(current_key_bin, pc1)
    key_left = current_key_bin[:28]
    key_right = current_key_bin[28:]
    for i in range(0, r):
        key_left = move(key_left, -1)
        key_right = move(key_right, -1)
        key = translation(key_left + key_right, pc2)
        secret_key.append(key)


def wheel_structure(left, right, current_round, types):
    if types == 1:
        key = secret_key[current_round]
    else:
        key = secret_key[-(current_round+1)]
    temp2 = right
    right = xor(left, func_f(right, key))
    left = temp2
    return left, right


def encode(plain_texts, rounds, key, types):
    generate_secret(key, rounds)
    plain_texts = change_hex_to_bin(plain_texts)
    plain_texts = translation(plain_texts, ip)
    cipher_text = ''
    left = plain_texts[:32]
    right = plain_texts[32:]
    for i in range(0, rounds):
        left, right = wheel_structure(left, right, i, types)
    cipher_text += right + left
    cipher_text = translation(cipher_text, ip_)
    cipher_text = hex(int(cipher_text, 2))[2:].upper().rjust(16, '0')
    return cipher_text


def main(texts, s_key, s_rounds, ty):
    c_texts = ''
    if ty == 1:
        print('要加密的明文为：', texts)
        for i in range(0, len(texts), 16):
            c_texts += encode(texts[i:i+16].ljust(16, '0').upper(), int(s_rounds), s_key, ty)
        print('密文：', c_texts)
    else:
        print('要解密的密文为：', texts)
        for i in range(0, len(texts), 16):
            c_texts += encode(texts[i:i+16].ljust(16, '0').upper(), int(s_rounds), s_key, ty)
        print('明文：', c_texts)
    return c_texts


if __name__ == '__main__':
    secret_key = []
    path = ''
    types1 = int(input('加密or解密(加密:1,解密:2)'))
    types2 = int(input('字符串or文件(字符串:1,文件:2)'))
    if types2 == 1:
        if types1 == 1:
            plain_text = input('请输入要加密的明文(16的倍数个十六进制数字符串):')
        else:
            plain_text = input('请输入要解密的密文(16的倍数个十六进制数字符串):')
    else:
        path = input('请输入文件的路径(文件内容必须为16的倍数个十六进制数字符串):')
        with open(path, 'r') as pl:
            plain_text = pl.read()
    if types1 == 1:
        keys = input('请输入加密密钥(16个十六进制数字符串):')
    else:
        keys = input('请输入解密密钥(16个十六进制数字符串):')
    round_s = input('请输入轮数:')
    text = main(plain_text, keys, round_s, types1)
    if types2 != 1:
        with open(path, 'w') as pl:
            pl.write(text)
