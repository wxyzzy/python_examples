# Example of using a decorator where the decorator
# calls the decorated function multiple times.


def multiple(func):
    def inner(a, b):
        a = a if type(a) in (list, tuple) else [a]
        b = b if type(b) in (list, tuple) else [b]
        for i in a:
            for j in b:
                func(i, j)
        return
    return inner


@multiple
def divide(a, b):
    print(a/b)


divide(2, 3)
divide((5, 10), [1, 2, 3])
