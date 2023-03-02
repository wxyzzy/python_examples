# How the range() function might be implemented


def range2(a, b = None):
    i, n = (0, a) if b is None else (a, b)
    while i < n:
        yield i
        i += 1


print ([x for x in range2(5)])

print ([x for x in range2(5, 10)])


# example use of iter() built-in function
ii = iter(range2(5))
while True:
    try:
        x = next(ii)
    except StopIteration:
        break
    print(x)
