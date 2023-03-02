# Tuples are immutable objects that are very useful.

tpl = ('How', 'do', 'you', 'do?')
print()
print('Here is the tuple:')
print(tpl)

# Here we print various slices
print()
print('Here we print various subsets of the list:')
print(tpl[:3])
print(tpl[1:])
print(tpl[::2])
print(tpl[::3])

# Here we print the entire list:
print()
print('Here we print the entire list one item at a time:')
for item in tpl:
    print(item)
