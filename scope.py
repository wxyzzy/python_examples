# Shows scope rules


# Global variables
a = 'whatever'
b = 'jojo'


def foo():
    #global a
    a = 'duh'
    print(a)
    print(b)


foo()
print(a)

