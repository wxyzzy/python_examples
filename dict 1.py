# Dictionaries are mutable objects that are very useful.

dct = {'How': 'I', 'are': 'am', 'you': 'doing', 'doing': 'fine'}
print()
print('Here is the dictionary:')
print(dct)
print(dct.keys())
print(dct.values())
print(dct.items())

# Here we use help from tuples and string functions:
print()
print('Here we print the entire dict one item at a time:')
for par in dct.items():
    k, v = par
    print(par)
    print('    {}: {}'.format(k, v))
