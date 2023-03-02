# Lists are mutable objects that are very useful.

lst = ['How', 'do', 'you', 'do?']
print()
print('Here is the list:')
print(lst)

# Here we print various slices of the list.print()
print()
print('Here we print various subsets of the list:')
print(lst[:3])
print(lst[1:])
print(lst[::2])
print(lst[::3])

# Here we print the entire list:
print()
print('Here we print the entire list one item at a time:')
for item in lst:
    print(item)
