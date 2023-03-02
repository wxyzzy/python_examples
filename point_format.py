# special method class Point.__format_
# note that (class variable) dictionary _format is required


from math import sqrt, atan, atan2, pi


class Point:
    _format = {"cart":"({}, {})", "polar":"({:.2f}, {:.5f})"}
    
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return ('Point({}, {})'.format(self.x, self.y))

    def length(self):
        return sqrt(self.x * self.x + self.y * self.y)

    @staticmethod
    def to_polar(x, y):
        r = sqrt(x**2 + y**2)
        theta = atan2(y, x) if y >= 0 else 2*pi + atan2(y, x)
        return r, theta
    
    def __format__(self,key):
        if key=="" or key=="cart":
            return self._format["cart"].format(self.x, self.y)
        else:
            return self._format["polar"].format(*self.to_polar(self.x, self.y))

if __name__ == "__main__":
    p0 = Point(0, 0)
    p1 = Point(5, -0.01)
    p2 = Point(0.01, 8)
    p3 = Point(0, 7)
    p4 = Point(-7, -0.01)
    
    print(f"pi = {pi:.5f}")

    print('Mapping from cartesian to polar')
    print('{:cart} -> {:polar}'.format(p0, p0))
    print('{:cart} -> {:polar}'.format(p1, p1))
    print('{:cart} -> {:polar}'.format(p2, p2))

    # the following syntax works as of Python 3.6
    print(f'{p3:cart} -> {p3:polar}')
    print(f'{p4:cart} -> {p4:polar}')
