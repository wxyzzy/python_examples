# Example of using a decorator design pattern


def trivial(func):
    def inner(a, b):
        print('Using the decorator design pattern')
        return func(a, b)
    return inner


def divide(a, b):
    print(a/b)


divide = trivial(divide)


divide(2, 3)
