# example of computing factorials


def factorial2(x):
    result = 1
    while x > 0:
        result *= x
        x -= 1
    return result

def test_factorial():
    print('Compare computation of factorial from module "math" ' +
          'and our local function.')
    from math import factorial
    d = {i:(factorial(i), factorial2(i)) for i in range(1, 8)}
    print('{}\t{}\t{}'.format('n', 'math', 'local'))
    for n in d:
        print('{}\t{}\t{}'.format(n, factorial(n), factorial2(n)))

if __name__ == "__main__":
    test_factorial()
