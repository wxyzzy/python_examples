# Study the Taylor series

from math import e, factorial
x = 3

def taylor_for_e(x, n):
    # n - provides the order of the last term in the series.
    result = 0
    i = 0
    while i <= n:
        result += x ** i / factorial(i)
        i += 1
    return result

def alternate_e(x, n):
    # n - used in this direct calculation
    return ((1 + 1 / n) ** n) ** x
    
def compare_taylor_and_e():
    print('Compare Taylor series approximation with constant e')
    print('Using n terms.')
    d = {k:taylor_for_e(x, k) for k in range(1, 15)}
    print('n^x\ttaylor(x,n)')
    for n in d:
        print(f'{n}\t{d[n]}')
    print(f'math.e =  {e ** x}')
    print(f'alternate {alternate_e(x, 1000000)}')


compare_taylor_and_e()
