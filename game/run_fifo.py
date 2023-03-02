# save function call in a blocking queue
# the called function is responsible to unblock the queue when it is done.


import time
from datetime import datetime
import time

start_time = round(time.time() * 1000)
milliseconds = lambda: round(time.time() * 1000) - start_time


class RunFifo:
    def __init__(self):
        global app_fifo
        app_fifo = self
        self.fifo = []
        self.flag = 'run'
        self.final = None
        self.verbose = False
        self.blocking_time = None
    
    def __str__(self):
        s = self.final[0] if self.final else "'none'"
        return f"RunFifo(flag:'{self.flag}', length:{len(self.fifo)}, final:{s}"
    
    @staticmethod
    def unpack(foo):
        # foo may be a function or a tuple(function, p, kw) of length 1, 2, or 3
        p, kw = tuple(), {}   # default values in case they are missing
        foo = foo if type(foo) in (tuple, list) else (foo,)
        n = len(foo)
        foo, p, kw = foo if n == 3 else (*foo, kw) if n == 2 else (*foo, p, kw)
        return foo, p, kw            
    
    def append(self, foo, *p, **kw):
        if len(self.fifo) > 5:
            return
        self.fifo.append((foo, p, kw))
        if self.verbose: print(f'fifo.append [{len(self.fifo)}]:', foo.__name__, p, kw)
        self._run_if_free()
    
    def _run_if_free(self):
        if self.flag == 'run' and self.fifo:
            self.flag = 'block'
            foo = self.fifo.pop(0)
            foo, p, kw = RunFifo.unpack(foo)
            if self.verbose: print(f'fifo.run [{len(self.fifo)}]:', foo.__name__, p, kw)
            self.blocking_time = milliseconds() + 50
            foo(*p, **kw)

    def run(self):
        self.flag = 'run'
        self.blocking_time = None
        self._run_if_free()

    def block(self, ms=None):
        self.flag = 'block'
        if ms:
            self.keep_blocking(ms)
    
    def keep_blocking(self, ms):
        if self.verbose: print('+', end='')
        self.blocking_time = milliseconds() + ms
        
    def set_completion_routine(self, final, *p, **kw):
        # called from within a function when it is run
        assert (not self.final), "RunFifo: only one completion routine may be defined"
        self.final = (final, p, kw)
        
    def complete_if_timed_out(self):
        #if (len(self.fifo) == 0 and not self.final
            #and (self.blocking_time or self.flag != 'run')):
            #if self.verbose: print('fifo is empty:')
            #self.blocking_time = None
            #self.flag = 'run'
        if not self.blocking_time:
            if self.verbose: print('fifo has no blocking_time:')
            self.complete()
        elif milliseconds() > self.blocking_time:
            if self.verbose: print('fifo is past blocking_time')
            self.complete()
        else:
            if False and self.verbose: 
                print('.', end='')
                time.sleep(0.5)
            
    def complete(self):
        if self.final:
            final, p, kw = RunFifo.unpack(self.final)
            if self.verbose: print('fifo.complete: run', final.__name__, p, kw)
            self.final = None
            final(*p, **kw)
        elif self.verbose:
            print('fifo.complete')
        self.run()

# app_fifo has to be set by app if multiple fifos in use
app_fifo = None    # reference to app's fifo

def fifo_run_queue(foo):
    def inner(*p, **kw):
        app_fifo.append(foo, *p, **kw)
    return inner


if __name__ == "__main__":
    
    fifo = RunFifo()    
    fifo.verbose = True
    
    def complete_this(msg):
        print('complete_this:', msg)
    
    @fifo_run_queue
    def do_this(*p, **kw):
        fifo.set_completion_routine(complete_this, 'Hello, this is done')
        print('do_this:', p, kw)
    
    @fifo_run_queue
    def do_other(*p, **kw):
        print('do_other:', p, kw)
    
    fifo.block()
    do_this(1, 2, 3)
    do_other('that', 'other', height=800)
    
    print('before call to fifo.complete')
    fifo.run()
    fifo.block(2000)
    while fifo.flag == 'block':
        fifo.complete_if_timed_out()
    fifo.complete()
    print(fifo)
    print('done')



