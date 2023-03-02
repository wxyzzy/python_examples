# There are many ways to get a list

lst1 = ['How', 'do', 'you', 'do?']
tup = 'I', 'am', 'very', 'fine'
lst2 = list(tup)
dic = {lst1[i]: lst2[i] for i in range(len(lst1))}
lst3 = list(dic.keys())
lst4 = list(dic.values())
lst5 = list(dic.items())

# Here we print the various lists

from pprint import pprint
pprint([lst1, lst2, lst3, lst4, lst5])

# Print as sentence
print()
print(' '.join(lst1))
print(' '.join(lst2))


