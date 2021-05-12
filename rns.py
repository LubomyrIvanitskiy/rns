import numpy as np
from itertools import accumulate


def _printer(i, a, m, k, m_a, k_a, z, x):
    print(f"{a}x%{m}={k}")
    print(f"x_{i}={x}")
    print()


def solve(a, m, k, i=0, prnt=False, allow_zero=False):
    """
    Solve simple linear conguruence equation
    Find the least x such that ax=k (mod m)
    if allow_zero=True 2x%3=0, x=0
    if allow_zero=False 2x%3=0, x=3
    """

    if m > k:
        if k == a == 0:
            return k
        elif k % a == 0:
            return k // a

    assert a > 0

    k_a = k % a
    m_a = m % a
    m_a = m_a if m_a > 0 else a
    z = a - k_a
    z = z if z > 0 else a

    if a == 1:
        x = k % m
        if not allow_zero:
            x = x if x > 0 else k
        if prnt:
            print('case 1')
            _printer(i, a, m, k, m_a, k_a, z, x)
        return x

    if m % a == 0:
        if k % m % a == 0:
            x = k % m // a
            if not allow_zero:
                x = x if x > 0 else k // a
            if prnt:
                print('case 2')
                _printer(i, a, m, k, m_a, k_a, z, x)
            return x
        else:
            print(f"{a}x%{m}={k} - No SOLUTIONS")
            raise ValueError('No solutions')

    new_x = solve(
        a=m_a,
        m=a,
        k=z,
        i=i + 1,
        prnt=prnt,
        allow_zero=allow_zero
    )
    x = (k + new_x * m) // a
    if prnt:
        print('case 3')
        _printer(i, a, m, k, m_a, k_a, z, x)
    return x


def get_dynamic_range(P):
    """
    Return the maximum integer numbers that can be uniquely encoded given moduli P

    >>> get_dynamic_range([7,6,5])
    210
    >>> get_dynamic_range([4,3,2])
    12
    """
    return np.lcm.reduce(P)


def encode(n, P):
    """
    Encode an integer decimal number n into corresponding RNS array
    >>> encode(n=14221, P=[21,19,18,11,10,8,7,5,4])
    [4, 9, 1, 9, 1, 5, 4, 1, 1]
    """
    if n >= get_dynamic_range(P):
        raise ValueError("You cannot encode such a big number with given moduli. Try to increase moduli dynamic range")
    code = [n % P[-i] for i in range(1, len(P) + 1)][::-1]
    return code


def decode(code, P):
    """
    Decode an RNS representation array into decimal number
    :param P: list of moduli in order from bigger to smaller [pn, .., p2, p1, p0]

    >>> decode(code=[5, 3, 1], P=[7,6,5])
    201
    """
    lcms = np.fromiter(accumulate(P[::-1], np.lcm), int)[::-1]

    n = code[-1] % P[-1]

    for i in range(1, len(P)):

        bottom_p = lcms[-i]

        per_diff = bottom_p % P[-i - 1]  # rev

        current_next = n % P[-i - 1]
        wanted_next = code[-i - 1] % P[-i - 1]
        if wanted_next < current_next:
            wanted_next = wanted_next + P[-i - 1]

        distance = wanted_next - current_next

        distance = distance % P[-i - 1]
        if distance > 0:
            bottomp_scroll_count = solve(a=per_diff, m=P[-i - 1], k=distance, allow_zero=True)
            n = n + bottomp_scroll_count * bottom_p

    return n


def list_encodings(P):
    """
    An utility method to get a list of all numbers n from 0 to get_dynamic_range(P) in RNS representation
    :param P: moduli, max(moduli) should be less than 32
    :return:
    """
    A = '0123456789ABCDEFGHJKLMNOPQRSTXYZ'
    max_value = get_dynamic_range(P)
    D = [A[:P[i]] * (max_value // P[i]) for i in range(len(P))]

    codes = []
    for code in zip(*D):
        codes.append(''.join(code))
    return codes


if __name__ == '__main__':
    from doctest import testmod

    testmod(name="decode", verbose=True)
