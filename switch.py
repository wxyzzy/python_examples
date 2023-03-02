# example of "switch" control statement in Python
# (which does not exist)
# The "Pythonic" way of doing this is with a dictionary


def contraction_of (k, v):
    print('{} is a contraction of {}'.format(k, v))

def jackie(): contraction_of ('jackie', 'jack')
def joey(): contraction_of ('joey', 'joe')
def jo(): contraction_of ('jo', 'jolinda')

switcher = {'jackie': jackie, 'joey': joey, 'jo': jo}

def foo(name):
    if name in switcher:
        switcher[name]()
    else:
        print('{} is not known'.format(name))


foo('sam')
foo('joey')
foo('jo')
foo('emil')
