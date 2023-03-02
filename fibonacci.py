# prints the Fibonacci series
# demonstrates "while" loop.


print('Fibonacci series')


def fib(n):
    a, b = 0, 1
    r = []
    while a < n:
        print(a, end=' ')
        if a > 0:
            r.append('{:.4f}'.format(b/a))
        a, b = b, a+b
    print()
    print('Ratio b/a:', end=' ')
    print(r)
    print('golden ratio: 1.618034')


fib(100)
