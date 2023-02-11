# A Python 3 script trying to in include every bytecode in Python 3.12, but it actually misses these bytecode:
# {'LOAD_ASSERTION_ERROR', 'CHECK_EG_MATCH', 'UNPACK_EX', 'POP_JUMP_BACKWARD_IF_NONE', 'DELETE_DEREF', 'POP_JUMP_FORWARD_IF_NOT_NONE', 'EXTENDED_ARG', 'PRINT_EXPR', 'LOAD_CLASSDEREF', 'MAP_ADD', 'POP_JUMP_BACKWARD_IF_NOT_NONE', 'JUMP_IF_FALSE_OR_POP', 'IS_OP', 'LIST_TO_TUPLE', 'JUMP_IF_TRUE_OR_POP', 'PREP_RERAISE_STAR'}
# the idea comes from https://github.com/kholia/dedrop
exit()
def main():

  (lambda:1)()

  zzz = 1
  del zzz

  a = 1; b = 2
  (a, b) = (b, a)

  a = 1
  (a, a, a) = (a, a, a)

  {'a':1}

  x = list(range(6))
  x[2:4] += 'abc'

  a = 1
  a = +a

  a = 1
  a = -a

  a = 1
  a = not a

  a = 1

  a = 1
  a = ~a

  a = [i*i for i in (1,2)]

  a = 2
  a = a ** 2

  a = 2
  a = a * 2

  a = 2
  a = a / 2

  a = 2
  a = a % 2

  a = 2
  a = a + 2

  a = 2
  a = a - 2

  a = [1]
  a[0]

  a = 2
  a = a // 2

  a = 2
  a = a / 2
  a = a // 2

  a = 1
  a //= 10.2

  a = 1
  a /= 2
  a //= 2
  b = 2
  a //= b
  a /= b

  a = [1,2,3]
  a = a[:]


  a = [1,2,3]
  a = a[1:]

  a = [1,2,3]
  a = a[:2]

  a = [1,2,3]
  a = a[1:2]

  a = [1,2,3]
  a[:] = [1,2,3]

  a = [1,2,3]
  a[1:] = [2,3]

  a = [1,2,3]
  a[:2] = [1,2]

  a = [1,2,3]
  a[1:2] = [2]

  a = [1,2,3]
  del a[:]

  a = [1,2,3]
  del a[1:]

  a = [1,2,3]
  del a[:2]


  a = [1,2,3]
  del a[1:2]

  a = 1
  a += 1

  a = 1
  a -= 1

  a = 1
  a *= 1

  a = 1
  a /= 1

  a = 1
  a %= 1

  a = [0, 1]
  a[0] = 1

  a = [1]
  del a[0]

  a = 1
  a = a << 1

  a = 1
  a = a >> 1

  a = 1
  a = a & 1

  a = 1
  a = a ^ 1

  a = 1
  a = a | 1

  a = 1
  a **= 1

  for a in (1,2): pass

  print("hello world!")

  print()

  def fv(a,b): pass
  av = (1,2)
  fv(*av)

  def fkv(a,b,c): pass
  akv = {"b":1,"c":2}
  b = (3,)
  fkv(*b, **akv)

  def fk(a,b): pass
  ak = {"a":1,"b":2}
  fk(**ak)


  import sys
  print("hello world", end=' ', file=sys.stdout)

  import sys
  print(file=sys.stdout)
  del sys.api_version

  zzz = 89
  del zzz


  a = 1
  a <<= 1

  a = 1
  a >>= 1

  a = 1
  a &= 1

  a = 1
  a ^= 1

  a = 1
  a |= 1

  for a in (1,2): break

  try:
    with open("1.txt") as f:
      print(f.read())
  except:
      pass

  class a: pass

  # empty file

  exec("print('hello world')", globals(), locals())

  frozenset({1, 2, 3})

  for a in (1,2): break

  try:
    a = 1
  except ValueError:
    a = 2
  finally:
    a = 3

  class a: pass

  a = 1

  a = 1
  del a

  (a, b) = "ab"

  for i in (1,2): pass

  a = 0
  b = [0]
  b[a] += 1

  a = 1

  a = 1
  a = a

  a = 1;
  a = (a, a)

  [1,2,3]

  {"a":1,"b":2}

  [].sort()

  a = 1 == 2

  a = 2+3+4
  "@"*4
  a="abc" + "def"
  a = 3**4
  a = 13//4

  a //= 2

  from dis import opmap

  if 1 == 2: pass
  else: pass

  if 1 == 2: pass
  else: pass

  if not(1 == 2): pass
  else: pass

  for i in (1,2): pass

  for x in (1,2):
    try: continue
    except: pass

  while 0 > 1: pass

  try:
    a = 1
  except ValueError:
    a = 2
  finally:
    a = 3

  try:
    a = 1
  except ValueError:
    a = 2
  finally:
    a = 3

  a = [1,2,3,4]
  b = a[::-1]

  xyz = 0

  def lolcats():
    global xyz
    pass

  raise ValueError


def fc():
  a = 1
  zyx = set()
  zyx.add("hello")
  zyx.add("abc")
  zyx.remove("hello")
  def g():
    return a + 1
  return g()

print(fc())


def f(): pass
f()


def f1():
  from sys import environ
  a = 1
  a = a

def f2():
  a = 1
  a = a

def f3():
  a = 1
  del a


import sys
sys.stderr = sys.stdout

import sys
# del sys.stderr

l1 = 0
def lolx():
  global l1
  l1 = 1

l2 = 0
def loly():
  global l2
  del l2
  def f():
    a = 3
    b = 5
    def g():
      return a + b
  f()

  mylist = [1, 1, 1, 2, 2, 3]
  z = {x for x in mylist if mylist.count(x) >= 2}
  a = {x for x in 'abracadabra' if x not in 'abc'}
  set([20, 0])

lolx()
loly()

def foo():
        print('hello')
        yield 1
        print('world')
        yield 2

a = foo()
print(next(a))
print(next(a))


def myfunc(alist: list):
    return len(alist)

def peko(*args, **kwargs):
    yield from f()
    1
    2
    3
    if True:
        return 1
    1
    2
    3
    pass

async def f():
    await f()
    async for x in f():
        pass

async def g():
    await g()
    yield 1
    async with x:
        pass

class A:
    n: int
a = 1
match a:
    case 1: print(1)
    case []: pass
    case A(): pass
    case {1:a}: pass

peko(*[123])
peko(**{'a':1})
peko(*[123], **{'a':1})
(x for x in [])
dt={}
dt|={'1':123}
f'1{2}3'
{**{1:2}}
tuple([1,2,3])
del a
from os import *
peko(*[1,2,3,4,5,6,7,8,9])
assert True
class A:
    pass

main()
