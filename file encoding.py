# This scipt shows file encoding


def foo1(s):
    f = open('temp1.txt', 'w', encoding="latin-1")
    f.write(s)
    f.close()


def foo2(s):
    f = open('temp2.txt', 'w', encoding="utf-8")
    f.write(s)
    f.close()


def foo3(s):
    f = open('temp3.txt', 'w', encoding="utf-16")
    f.write(s)
    f.close()


foo1('töst sträng')
foo2('töst sträng')
foo3('töst sträng')
