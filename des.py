from table import ip, ip_, pc1, pc2, table_e, table_p, s_box
secret_key = []


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


def generate_secret(key_left, key_right):
    key_left = move(key_left, -1)
    key_right = move(key_right, -1)
    key = translation(key_left + key_right, pc2)
    secret_key.append(key)
    return key_left, key_right, key


def wheel_structure(left, right, key_left, key_right, r, ty):
    for i in range(0, r):
        if ty == 1:
            key_left, key_right, key = generate_secret(key_left, key_right)
        else:
            key = secret_key[-1]
            secret_key.pop()
        temp2 = right
        right = xor(left, func_f(right, key))
        left = temp2
    return left, right


def encode(plain_text, r, current_key, ty):
    plain_text = change_hex_to_bin(plain_text)
    plain_text = translation(plain_text, ip)
    cipher_text = ''
    left = plain_text[:32]
    right = plain_text[32:]
    current_key_bin = bin(int(str(current_key), 16))[2:].rjust(64, '0')
    current_key_bin = translation(current_key_bin, pc1)
    key_left = current_key_bin[:28]
    key_right = current_key_bin[28:]
    left, right = wheel_structure(left, right, key_left, key_right, r, ty)
    cipher_text += right + left
    cipher_text = translation(cipher_text, ip_)
    cipher_text = hex(int(cipher_text, 2))[2:].upper().rjust(16, '0')
    return cipher_text


def main():
    # a = input('请输入要加密的16个十六进制数字符串:')
    # key = input('请输入加密密钥(16个十六进制数字符串:)')
    # r = input('请输入加密轮数:')
    r = 16
    a = '123A06C0AFE0910F'
    key = '216AFE9B4106DCC0'
    print('要加密的明文为：', a)
    a = encode(a, r, key, 1)
    print('密文：', a)
    a = encode(a, r, key, 0)
    print('解密后的明文：', a)


if __name__ == '__main__':
    main()
