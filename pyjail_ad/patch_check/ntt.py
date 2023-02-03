from typing import List


def inv(x: int, p: int) -> int:
    return pow(x, -1, p)


def prim_root(p: int) -> int:
    # assuming p is prime
    for i in range(2, p):
        if pow(i, (p - 1) // 2, p) != 1:
            return i


def roots_of_unity(x: int, p: int) -> int:
    # assuming p is prime
    assert (p - 1) % x == 0
    f = (p - 1) // x
    return pow(prim_root(p), f, p)


def evaluate(f: List[int], w: int, p: int) -> List[int]:
    # evaulate polynomial represented by `f`` at `w^0, w^1, w^2, ...` modulo `p``
    # assuming len(f) is power of 2
    n = len(f)
    if n == 1:
        return f
    w2 = (w * w) % p
    even = evaluate(f[::2], w2, p)  # [even(w^0), even(w^2), even(w^4), ...]
    odd = evaluate(f[1::2], w2, p)  # [odd(w^0), odd(w^2), odd(w^4), ...]
    ar = [0] * n

    # original:
    # for i in range(n):
    #     j = i % len(even)
    #     ar[i] = (even[j] + pow(w, i, p) * odd[j]) % p

    x = 1
    for i in range(n // 2):
        ar[i] = (even[i] + x * odd[i]) % p
        ar[i + n // 2] = (even[i] - x * odd[i]) % p
        x = (x * w) % p
    return ar


def ntt(f: List[int], p: int) -> List[int]:
    w = roots_of_unity(len(f), p)
    return evaluate(f, w, p)


def intt(f: List[int], p: int) -> List[int]:
    w = roots_of_unity(len(f), p)
    ninv = inv(len(f), p)
    return [(x * ninv) % p for x in evaluate(f, inv(w, p), p)]


def polymul(a: List[int], b: List[int], p: int) -> List[int]:
    n = len(a) + len(b)
    m = 1
    while m < n:
        m *= 2
    a += [0] * (m - len(a))
    b += [0] * (m - len(b))
    return intt([(x * y) % p for x, y in zip(ntt(a, p), ntt(b, p))], p)


p = 65537
ar = [1, 8, 3, 4, 9, 2, 7, 6]

print(ntt(ar, p))
print(intt(ntt(ar, p), p))
print(polymul([1, 2, 1], [1, 2, 1], p))
