# Example use of namedtuples


from collections import namedtuple


# Create a namedtuple type (class), Point
Point = namedtuple("Point", "x y")

# Instantiate the new type
point1 = Point(2, 4)
point2 = Point(x=22, y=44)

# Use the points
print(type(point1))
print(point1)
print(point2)
print(point1.x, point1.y)
point1.x = 5
