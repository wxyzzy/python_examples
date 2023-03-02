# This shows operator overloading
# see, https://docs.python.org/3/library/operator.html

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __mul__(self, other):
        if type(other) in [int, float]:
            x = self.x * other
            y = self.y * other
        else:
            x = self.x * other.x
            y = self.y * other.y
        return Point(x, y)


a = Point(2, 3)
b = Point(3, 4)
print(a + b)
print(a * b)
print(a * 2)
print(a * 2.5)
print(b.y)
