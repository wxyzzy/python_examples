# How the __iter__ and __next__ methods work to make an iterable class
# See also yield3.py


class Range3:
    def __init__(self, a, b = None):
        self.a, self.n = (0, a) if b is None else (a, b)
       
    def __iter__(self):
        self.i = self.a - 1
        return self

    def __next__(self):
        self.i += 1
        if self.i >= self.n:
            raise StopIteration
        return self.i


if __name__ == "__main__":
	obj = Range3(5)
	print ([x for x in obj])
	print ([x for x in Range3(5, 10)])


	# example use of iter() built-in function
	ii = iter(obj)
	while True:
		try:
			x = next(ii)
		except StopIteration:
			break
		print(x)
