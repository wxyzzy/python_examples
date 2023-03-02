# multiplication table - pythonic

lst = [[x*y for x in range(1, 10)] for y in range(1, 10)]
print(lst)
s = '\n'.join(['\t'.join([str(a) for a in b]) for b in lst])
print(s)


# note: we can substitude lst to make this 2 lines and
# substitute s to make this one line.
