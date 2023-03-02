# This shows how to use a lambda function


def print_table(foo, title):
    print(title)
    lst = [[foo(x, y) for x in range(1, 10)] for y in range(1, 10)]
    print(lst)
    s = '\t' + '\t'.join([str(i) for i in range(1, 10)]) + '\n'
    i = 0
    for b in lst:
        i += 1
        s += '{}\t'.format(i)
        s += '\t'.join([str(a) for a in b]) + '\n'
    print(s)


print_table(lambda a,b: a*b,  'multiplikation')
print_table(lambda a,b: a+b,  'addition')
print_table(lambda a,b: a//b, 'integer division')
print_table(lambda a,b: a%b,  'modulo')
