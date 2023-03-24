# Example of using a decorator - trivial


def trivial(func):
    print('set up decorator one')
    def inner(*c):
        print('Using decorator one:')
        return func(*c)
    return inner

def trivial2(func):
    print('set up decorator two')
    def inner(*c):
        print('Using decorator two:')
        return func(*c)
    return inner


@trivial
@trivial2
def divide(a, b):
    print(a/b)


divide(9, 3)
