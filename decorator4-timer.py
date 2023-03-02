# Example of using a decorator where the decorator calls
# a function that returns every second with some information.


import time
from datetime import datetime


def everysecond(func):
    def inner(t=0):
        while True:
            time.sleep(1.0)
            t = datetime.now()
            func(t)
        return
    return inner


@everysecond
def do_something(t):
    print('time: {}'.format(t))


do_something()

