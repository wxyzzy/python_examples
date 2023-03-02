# Example of using a decorator where the decorator saves a
# function call in a queue.


import time
from datetime import datetime

class RunFifo:
    def __init__(self):
        self.fifo = []
        self.flag = 'run'

    @staticmethod
    def unpack(foo):
        # foo may be a function or a tuple(function, p, kw) of length 1, 2, or 3
        p, kw = tuple(), {}   # default values in case they are missing
        foo = foo if type(foo) in (tuple, list) else (foo,)
        n = len(foo)
        foo, p, kw = foo if n == 3 else (*foo, kw) if n == 2 else (*foo, p, kw)
        return foo, p, kw            

    def append(self, foo, *p, **kw):
        self.fifo.append((foo, p, kw))
        self.run()
    
    def run(self):
        if self.flag == 'run' and self.fifo:
            self.flag = 'block'
            foo = self.fifo.pop(0)
            foo, p, kw = RunFifo.unpack(foo)
            self.final = kw.pop('fifo_complete') if 'fifo_complete' in kw else None
            foo(*p, **kw)

    def complete(self):
        if self.final:
            final, p, kw = RunFifo.unpack(self.final)
            self.final = None
            final(*p, **kw)
        self.flag = 'run'
        self.run()

def fifo_queue(foo):
    def inner(*p, **kw):
        fifo.append(foo, *p, **kw)
    return inner
        
fifo = RunFifo()



# The following lines are an example of use

def after_something(msg):
    print('after -', msg)

def do_something(*p, **kw):
    fifo.append(_do_something, *p, **kw, 
                fifo_complete = (after_something, ('my bad',)))

def _do_something(this, that, width):
    print('do_somthing: {}'.format(this))

do_something('thing', 'other', width=500)
fifo.complete()


# The following lines are an example of use

print()


@fifo_queue
def do_other(*p, **kw):
    print('other:', p, kw)

do_other('this', 'that', height=800)
fifo.complete()

print('done')



