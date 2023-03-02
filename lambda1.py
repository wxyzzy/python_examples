# This shows how to use a lambda function


def fmult1(a, b):
    z = a * b
    return z


def fmult2(a, b):
    return a * b


def fmult3(a, b): return a * b


fmult4 = lambda a, b: a * b


print(fmult1(3, 4))
print(fmult2(3, 4))
print(fmult3(3, 4))
print(fmult4(3, 4))

def my_print(foo, a, b):
    print(foo(a, b))
    
my_print(lambda a,b: a * b, 3, 4)
my_print(fmult3, 3, 40)
