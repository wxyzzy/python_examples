# The yield function makes this function a generator


# a trivial generator function
def feed_me(a):
    for x in a:
        yield '$' + x


a = ('moe', 'joe', 'julia', 'jane')
b = [x for x in feed_me(a)]
print(type(b))
print(b)

# example of creating a generator "g"
g = (x for x in feed_me(a))
print(type(g))
print(g)

# converting the generator to a tuple
d = tuple(g)
print(d)
