# "list comprehension" is pythonic


# traditional way:
lst2 = []
for x in range(1, 10):
    lst2.append(x)
print(lst2)


# pythonic way:
lst = [10*x for x in range(1, 10)]
print(lst)


# compose a string:
s = '\t'.join([str(10*a) for a in lst])
print(s)
