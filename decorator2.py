# Example of using a decorator - trivial


def trivial(func):
    def inner(*c):
        print('Using decorator syntax "@":')
        return func(*c)
    return inner


@trivial
def divide(a, b):
    print(a/b)


divide(2, 3)
