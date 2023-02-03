def mix_globals(**kwargs):
    def deorator(f):
        g = dict(f.__globals__)
        g.update(kwargs)
        return type(f)(f.__code__, g, f.__name__, f.__defaults__, f.__closure__)

    return deorator


def mix_closure(**kwargs):
    def deorator(f):
        fvs = f.__code__.co_freevars
        closure = list(f.__closure__)
        C = type(closure[0])
        for k, v in kwargs.items():
            closure[fvs.index(k)] = C(v)
        return type(f)(
            f.__code__, f.__globals__, f.__name__, f.__defaults__, tuple(closure)
        )

    return deorator


def wrap_print(*args, **kwargs):
    print(*["wrap_print", *args], **kwargs)


@mix_globals(print=wrap_print)
def add(a, b):
    """
    Add two numbers and print the result
    """
    print(f"Computing {a} + {b} = {a + b}")


add(1, 2)
print(add.__doc__)
print(add.__name__)


def closure_test():
    a = 1
    b = 2

    @mix_closure(a=100)
    @mix_globals(print=wrap_print)
    def f():
        print(a + b)

    @mix_globals(print=wrap_print)
    @mix_closure(a=100)
    def g():
        print(a + b)

    f()
    g()
    print(a, b)  # not modified


closure_test()
