# example class Point
# assignment: extend this with __add__ and __mul__

from math import sqrt


class Point:
    dim = 3   # number of dimensions of Point
    def __init__(self, x, y, z=0):
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        return ('Point({}, {}, {})'.format(self.x, self.y, self.z))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def length(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __gt__(self, other):
        return self.length() > other.length()

    def __lt__(self, other):
        return self.length() < other.length()

    def __le__(self, other):
        return (self.length() < other.length() or
                (self.x == other.x and self.y == other.y and self.z == other.z))
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


if __name__ == "__main__":
    p1 = Point(5, 0)
    p2 = Point(0, 8)
    d = p1.__dict__
    d1 = p1.__class__.__dict__
    print('class_dict: ', d1)
    d1 = {k: d1[k] for k in d1 if k[0] != '_' and type(d1[k]) in (int, float, str)}
    print('class_dict: ', d1)
    
    print(p1)
    print(p2)
    print('instance variables: ', d)
    print('class variables: ', d1)

    print('length p1: ' + str(p1.length()))
    print('p1 > p2? ', p1 > p2)
    print('p1 < p2? ', p1 < p2)
    print('p1 == p2? ', p1 == p2)

    print('p1 + p2: ', p1 + p2)
