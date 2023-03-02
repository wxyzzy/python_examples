# Refactor function fib(n) to a generator function and to a class:


def fib(n):
    a, b = 0, 1
    f = []
    while a < n:
        f.append(a)
        a, b = b, a+b
    return f

f = fib(100)
print(f)


def fib2(n):
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a+b

f = [x for x in fib2(100)]
print(f)


class Fibonacci:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        self.a, self.b = 0, 1
        return self
    def __next__(self):
        if self.a >= self.n:
            raise StopIteration()
        a0 = self.a
        self.a, self.b = self.b, self.a+self.b
        return a0

fobj = Fibonacci(100)
f = [a for a in fobj]
print(f)
