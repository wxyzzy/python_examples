

d = {1: 'one', 2: 'two', 5: 'five'}


def foo(dd):
    for x in dd.keys():
        yield (x, dd[x])


b = [x for x in foo(d)]
print(b)
