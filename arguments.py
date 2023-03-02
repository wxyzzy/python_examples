# Example to show positional and keyword arguments
# ref: https://stackoverflow.com/
#    questions/1419046/normal-arguments-vs-keyword-arguments


def foo(*positional, **keywords):
    print("Positional: ", positional)
    print("Keywords: ", keywords)


print("The *positional argument stores arguments in a tuple")
foo('one', 'two', 'three')

print()
print("The **keywords argument stores in a dictionary")
foo(a='uno', b='dos', c='tres')

print()
print("Positional arguments come before keyword arguments.")
foo('one', 'two', 'three', a='uno', b='dos', c='tres')


print()
print("unpack values from tuple and dictionary")
tup = 2, 3
dic = {'name': 'jojo', 'phone': '109237804'}
foo(*tup, **dic)
