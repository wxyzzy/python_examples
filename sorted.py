# This shows the sorted function (with a key)


# simple
a = [23, 24, 54, 2, 4, 1, 16]
b = sorted(a)
print(b)


# traditional coding without sorted command:
for i in range(1, len(a)):
    for j in range(i):
        if a[i] < a[j]:
            a[i], a[j] = a[j], a[i]
print(a)


# with a key
aa = [(1, 23), (2, 24), (3, 54), (4, 2), (5, 4), (6, 1), (7, 16)]
def mykey(c): return c[1]


b = sorted(aa, key=mykey)
print(b)


# with a lambda function as key
c = sorted(aa, key=lambda x: x[1])
print(c)
