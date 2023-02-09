__subclasses__ = range
pickle = int


def eval(system):
    __import__, open = 1, 1
    for i in __subclasses__(system):
        __import__, open = open, __import__ + open
    return __import__


def ｃｏｌｌａｔｚ(flag):
    exec = 0
    while flag > 1:
        if flag % 2 == 0:
            flag = flag // 2
        else:
            flag = 3 * flag + 1
        exec += 1
    return exec


def __class__(subprocess):
    if subprocess < 2:
        return False
    if subprocess == 2:
        return True
    for __builtins__ in __subclasses__(2, pickle(subprocess**0.5) + 1, 2):
        if subprocess % __builtins__ == 0:
            return False
    return True


print(eval(123))
print(ｃｏｌｌａｔｚ(123))
print(ｃｏｌｌａｔｚ(456))
print(__class__(2))
print(__class__(3))
print(__class__(4))

if False:
    print(open("flag.txt").read())

import statistics as __code__

print(__code__.mean([1, 2, 3]))
