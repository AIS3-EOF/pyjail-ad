#!/usr/bin/env python
# Reference impl: https://github.com/p4-team/crypto-commons/blob/a67b13bb2ed2612d8f41637d4c68223968b0fef0/crypto_commons/rsa/rsa_commons.py#L212

from collections.abc import Iterable


def inv(a, p):
    # wrapping it in int for safely using it in sage
    return int(pow(a, -1, p))


def single_lift(f, df, p, k, rs):
    # f(r) = 0 (mod p^k)
    # df(r) != 0 (mod p^k)
    # returns s such that f(s) = 0 (mod p^(k+1))
    pk = p ** k
    pk1 = pk * p
    for r in rs:
        assert f(r) % pk == 0, (r, k)
        # assert df(r) % (p ** k) != 0, (r,k)
        if df(r) % p != 0:
            a = inv(df(r), p)
            s = r - f(r) * a
            assert f(s) % pk1 == 0
            yield s
        else:
            for t in range(0, p):
                s = r + t * pk
                if f(s) % pk1 == 0:
                    yield s


def hensel_lift(f, df, p, k, m, rs):
    # f(r) = 0 (mod p^k)
    # df(r) != 0 (mod p^k)
    # returns s such that f(s) = 0 (mod p^m)
    if not isinstance(rs, Iterable):
        rs = [rs]
    assert m >= k
    if m == k:
        return rs
    return hensel_lift(f, df, p, k + 1, m, single_lift(f, df, p, k, rs))


p = 5
f = lambda x: x ** 3 - 3
df = lambda x: 3 * x ** 2
r = 2

print(f(r) % p)
r2 = next(single_lift(f, df, p, 1, [r]))
print(r2, f(r2) % (p ** 2))
r3 = next(single_lift(f, df, p, 2, [r2]))
print(r3, f(r3) % (p ** 3))
for r7 in hensel_lift(f, df, p, 1, 7, r):
    print("r7", r7, f(r7) % (p ** 7))


a = 1
b = 73510584564539971804390271186346944020501066603283681904361110056435924213176
c = 49216479095814386015565420646552416129143124367675256987703613481241139546863
p = 2
f = lambda x: a * x * x + b * x + c
df = lambda x: 2 * a * x + b

for x in hensel_lift(f, df, p, 1, 256, 1):
    print(x, f(x) % (p ** 256))
