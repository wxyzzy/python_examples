# iterators



fruit = ["apple", "banana", "cherry"]
key = ["a", "b", "c"]


d = {key[i]:x for i, x in enumerate(fruit)}
print(d)

lst = [(key[i], x) for i, x in enumerate(fruit)]
print(lst)
