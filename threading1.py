# This file shows an example of threading
# two threads that call each other and return a result


import threading
import time


a, b, x = 0, 1, 0
a0, b0, x0 = 0, 0, 0
stop = False


def mult(a, b):
    return a*b


def first_thread():
    global a, b, x, stop, a0, b0
    while not stop:
        if (a != a0 or b != b0):
            print('{}*{}'.format(a, b), end='')
            a0, b0 = a, b
            x = mult(a, b)
        time.sleep(0.01)


def second_thread():
    global a, b, x, stop, x0
    while not stop:
        if (x != x0):
            print('={}, '.format(x))
            x0 = x
            b += 1
        time.sleep(0.01)


def start_thread():
    t1 = threading.Thread(target=first_thread)
    t2 = threading.Thread(target=second_thread)
    t1.start()
    t2.start()


a = 23
b = 2
x = 0
start_thread()
while x0 <= 207:
    time.sleep(0.001)
stop = True
