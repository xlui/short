BASE62 = 'PnX6DWihwH8OAJklcaq9UVzNedBpSI3yCvMfbjstLZG7oK5YT2rEx01QmF4uRg'


def base10to62(x: int, alphabet=BASE62):
    if x == 0:
        return alphabet[0]
    res, base = [], len(alphabet)

    while x:
        x, rem = divmod(x, base)
        res.append(alphabet[rem])
    res.reverse()
    return ''.join(res)


def base62to10(x: str, alphabet=BASE62):
    digit, res, base = len(x), 0, len(alphabet)
    for c in x:
        res += alphabet.index(c) * (base ** (digit - 1))
        digit -= 1
    return res
