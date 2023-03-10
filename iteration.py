# Example of making a class an iterable.  From:
# https://www.programiz.com/python-programming/iterator


class PowTwo:
    """Class to implement an iterator
    of powers of two"""

    def __init__(self, max=0):
        self.max = max

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= self.max:
            result = 2 ** self.n
            self.n += 1
            return result
        else:
            raise StopIteration


if __name__ == "__main__":
    p2 = PowTwo(10)
    print([x for x in p2])
