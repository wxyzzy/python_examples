# develop mapping of position that moves slowly at beginning and end

from math import sin, pi, sqrt
import matplotlib.pyplot as plt  
import numpy as np
import random

def opt(d, key, default):
    return d[key] if key in d else default

def next_point_straight(p, p0, p1, s, steps):
    return p0 + (p1 - p0) * s / steps

map = None
def make_map(width, height, obstacles):
    def weight(p, ob):
        x, y = p; xo, yo = ob
        dx, dy = x - xo, y - yo
        if abs(dx) + abs(dy) > 15:
            return 0
        else:
            d = sqrt(dx ** 2 + dy ** 2)
            w = 10 if d < 5 else 2 if d < 10 else 0
            return w
    def f(x,y):
        w = sum([weight((x, y), ob) for ob in obstacles])
        return w
    map = [[f(x, y) for x in range(width)] for y in range(height)]
    return map

def init_point_weighted(width, height, n_obsticles):
    global map
    def position(w, h):
        x0, y0 = w // 10, h // 10
        x1, y1 = w - x0, h - y0
        return random.randint(x0, x1), random.randint(y0, y1)
    obsticles = [position(width, height) for i in range(n_obsticles)]
    map = make_map(width, height, obsticles)

def plot_map():
    import matplotlib.cm as cm
    global map
    width, height = len(map), len(map[0])
    delta = 1
    x = np.arange(0, width)
    y = np.arange(0, height)
    X, Y = np.meshgrid(x, y)
    #Z = np.asarray([[abs(j-width//2) + abs(i-height//2) for j in range(height)] for i in range(width)])
    Z = np.asarray([[map[j][i] for j in range(height)] for i in range(width)])
    fig, ax = plt.subplots()
    im = ax.imshow(Z, interpolation='bilinear', cmap=cm.RdYlGn,
                   origin='upper', extent=[0, width, 0, height],
                   vmax=abs(Z).max(), vmin=0)
    plt.show()
    
def next_point_weighted(p, p0, p1, s, steps):
    pass

def test_map():
    width, height = 100, 100
    n_obsticles = 5
    init_point_weighted(width, height, n_obsticles)
    plot_map()
    
class Fly:
    def __init__(self, *p, **options):
        # expect a, steps, starting point p0, and ending point p1
        self.accel = opt(options, 'accel', 1)
        self.steps = opt(options, 'steps', 100)
        self.next_point = opt(options, 'next_point', None)
        self.p0, self.p1 = np.asarray(p)

    def __iter__(self):
        self.p = self.p0.copy()
        self.lastp = self.p.copy()
        self.s = 0
        self.v = 0
        self.is_done = False
        return self

    def __next__(self):
        if self.is_done:
            raise StopIteration
        remainder = sqrt(sum((self.p1 - self.p)**2))
        while all(self.p == self.lastp) and any(self.p != self.p1) and remainder > 1:
            if self.accel > 0 and np.sum((self.p - self.p0)**2) > np.sum(((self.p1 - self.p0) / 2)**2):
                self.accel = -self.accel
            self.v = max(self.v + self.accel, 1)
            self.s += self.v            
            if self.next_point:
                self.p = self.next_point(self.p, self.p0, self.p1, self.s, self.steps)
            else:
                self.p = self.p0 + (self.p1 - self.p0) * self.s / self.steps
            remainder = sqrt(sum((self.p1 - self.p)**2))            
        if all(self.p == self.p1) or remainder <= 1:
            self.p = self.p1
            self.is_done = True
        self.lastp = self.p.copy()
        return tuple(self.p)
   
def test_fly_numpy():  
    x0, y0, x1, y1 = 0, -10, 100, 0
    fly = Fly((x0, y0), (x1, y1), next_point = next_point_straight)
    xx, yy = [], []
    for x, y in fly:
        print(f'{x:.2f}\t{y:.2f}')
        xx.append(x)
        yy.append(y)
    print(f'{x1:.2f}\t{y1:.2f}')
    xx.append(x1)
    yy.append(y1)
    plt.plot(xx, yy, 'o-')
    plt.show()

if __name__ == "__main__":
    #test_fly()
    test_fly_numpy()
    #test_map()
