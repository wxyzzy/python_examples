# More on Functions
# ref Peter Hoffmann,
# https://stackoverflow.com/questions/36901/what-does-double-star-asterisk-and-star-asterisk-do-for-parameters


print('Use of *args.')


def foo(*args):
    for a in args:
        print(a)


foo(1, 2, 3)


print('\nUse of **kwargs.')


def bar(**kwargs):
    for a in kwargs:
        print(a, kwargs[a])


bar(name='one', age=27)


print('\nUse of both *args and **kwargs.')


def car(*args, **kwargs):
    print(args)
    print(kwargs)


car(1, 2, 3, name='one', age=27)


print('\nUse of * in call to function.')


def foo(a, b, c):
    print(a, b, c)


aa = 100, 50, 20
foo(*aa)
