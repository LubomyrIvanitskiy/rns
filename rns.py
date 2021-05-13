from math import gcd


def _printer(i, a, m, k, x):
    print(f"{a}x%{m}={k}")
    print(f"x_{i}={x}")
    print()


def solve(a, m, k):
    """
    Solve simple linear conguruence equation
    Find the least x such that ax=k (mod m)
    if allow_zero=True 2x%3=0, x=0
    if allow_zero=False 2x%3=0, x=3
    """

    if a == 0:
        if k == 0:
            return 0
        else:
            raise ValueError(f"{a}x%{m}={k} - No SOLUTIONS")

    if a == 1:
        return k % m

    if k % a == 0:
        return k // a

    new_x = solve(
        a=m % a,
        m=a,
        k=(a - k) % a
    )
    x = (k + new_x * m) // a
    return x


def get_dynamic_range(P):
    """
    Return the maximum integer numbers that can be uniquely encoded given moduli P

    >>> get_dynamic_range([7,6,5])
    210
    >>> get_dynamic_range([4,3,2])
    12
    """
    r = 1
    for p in P:
        r = getLCM(r, p)
    return r


def encode(n, P, check_range=True):
    """
    Encode an integer decimal number n into corresponding RNS array
    >>> encode(n=14221, P=[21,19,18,11,10,8,7,5,4])
    [4, 9, 1, 9, 1, 5, 4, 1, 1]
    """
    if check_range and n >= get_dynamic_range(P):
        raise ValueError("You cannot encode such a big number with given moduli. Try to increase moduli dynamic range")
    return [(n % q) for q in P]


def getLCM(a, b):
    """
    :param a: int
    :param b: int
    :return: least common multiple
    """
    return a * b // gcd(a, b)


def decode(code, P, is_coprime=False):
    """
    Decode an RNS representation array into decimal number
    :param is_coprime: set it to True if you know the moduli is co-prime. It will speedup a computaion
    :param P: list of moduli in order from bigger to smaller [pn, .., p2, p1, p0]

    >>> decode(code=[5, 3, 1], P=[7,6,5])
    201
    """

    k = code[-1] % P[-1]
    lcm = 1

    for i in range(1, len(P)):
        c = code[-i - 1]
        a = P[-i - 1]

        distance = (c - k) % a
        if distance > 0:
            lcm = lcm * P[-i] if is_coprime else getLCM(lcm, P[-i])
            x = solve(a=lcm % a, m=a, k=distance)
            k = k + x * lcm

    return k


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
