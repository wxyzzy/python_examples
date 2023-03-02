"""
2D rocketry simulator
Erik Nash
This work is licensed under the Creative Commons Attribution 4.0 
International License. To view a copy of this license, 
visit http://creativecommons.org/licenses/by/4.0/ or send a letter 
to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

import numpy as np
import math
import tkinter as tk
import copy
import random

G = 1

def to_cartesian(r, angle):
    """returns numpy array cartesian coords representing
    the polar coords given"""
    return r*np.array([math.cos(angle), math.sin(angle)])

def to_polar(x):
    x, y = x[0], x[1]
    r = math.sqrt(x**2 + y**2)
    angle = math.acos(x/r)
    if y < 0: angle = -angle
    return r, angle


class Trace_mark:
    """a static marker"""
    def __init__(self, view, x, size = 3):
        self.x = x
        self.type = "trace_mark"
        self.size = size
        self.id = None
        self.view = view

    def draw(self):
        self.id = self.view.draw(self)

    def update(self, t):
        pass

    def delete(self):
        self.view.delete(self)


class Matter:
    """something that is affected by gravity"""
    def __init__(self, size, m, x, v, a = np.zeros(2), angle=0, anglev=0, anglea=0):
        self.x = x
        self.v = v
        self.a = a
        self.angle = angle
        self.anglev = anglev
        self.anglea = anglea
        self.m = m
        self.size = size
        self.type = None
        self.id = None
        self.color = "yellow"


    def direction(self, angle=0):
        angle = self.angle + angle
        return np.array([math.cos(angle), math.sin(angle)])

    def interaction(self, objects, sim):
        self.gravity(objects)

    def gravity(self, objects):
        """adds the contribution of the planets to the acceleration of this
        object"""
        planets = [obj for obj in objects if obj.type=="planet"]
        for p in planets:
            if p is self:
                continue
            r = p.getx() - self.x
            pm = p.getmass()
            self.a += r*G*pm/sum(r**2)**(3/2)

    def update(self,t):
        """increments position and angle by time t. More precise with lower t"""
        self.v += self.a*t
        self.x += self.v*t
        self.anglev += self.anglea*t
        self.angle += self.anglev*t
        self.a = 0

    def getmass(self):
        return self.m

    def getx(self):
        return self.x


class Rock(Matter):
    def __init__(self, size, m, x, v, color="yellow"):
        super().__init__(size, m, x, v)
        self.type = "rock"
        self.color=color


class Rocket(Matter):
    """Rocket object, has a variable thrust"""
    def __init__(self, m, x, v=np.zeros(2), angle=0, maxthrust=0.08,
                maxtwist=0.005, size=5, landed_on=None, color="yellow"):
        super().__init__(size, m, x, v, angle=angle)
        self.thrust = 0
        self.maxt = maxthrust
        self.twist = maxtwist
        self.type = "rocket"
        self.thrustid = None
        self.landed_on = landed_on
        self.color = color
        self.bullets = 3

    def interaction(self, objects, sim):
        if self.landed_on != None:
            return
        self.collision(objects, sim)
        super().interaction(objects, sim)

    def collision(self, objects, sim):
        for obj in objects:
            if obj is self:
                continue
            r = self.x - obj.x
            abs_r = math.sqrt(sum(r**2))
            if sim.collision and \
                        abs_r < self.size + obj.size:
                sim.crashed(self)
            if abs_r < self.size + obj.size + 5:
                self.check_landed(obj)

    def check_landed(self, obj):
        if self.thrust != 0 or self.landed_on !=None:
            return
        x = self.x - obj.x
        r, a = to_polar(x)
        if abs(self.angle-a) > 0.7: return
        vdiff = self.v - obj.v + obj.anglev*to_cartesian(r, a+math.pi/2)
        if math.sqrt(sum(vdiff**2))>2:
            return
        self.landing(obj, a)

    def landing(self, obj, angle=0, r="default"):
        self.landed_on = obj
        if r=="default": r = self.size + obj.size + 4
        self.x = obj.x + to_cartesian(r, angle)
        self.v = obj.v + obj.anglev*to_cartesian(r, angle + math.pi/2)
        self.angle = angle
        self.anglev = obj.anglev
        self.bullets = 3

    def update(self, t=1):
        if self.thrust != 0: self.landed_on = None
        if self.landed_on==None:
            self.a += self.thrust*self.direction()
            super().update(t)
        else:
            p = self.landed_on
            x = self.x - p.x
            r, a = to_polar(x)
            self.v = p.v + p.anglev*to_cartesian(r, a + math.pi/2)
            self.x = self.x + self.v
            self.angle += p.anglev

    def fire(self, size=5, speed=1):
        if self.bullets == 0:
            return
        self.bullets -= 1
        x = self.x + to_cartesian(self.size + size + 1, self.angle)
        v = self.v + to_cartesian(speed, self.angle)
        return Rock(size=5, m=1, x=x, v=v, color=self.color)

    def copy(self):
        """returns a copy of this rocket"""
        return Rocket(m=self.m, x=copy.copy(self.x),
                      v=copy.copy(self.v))

    def settwist(self, val):
        if val == "left":
            self.anglea = self.twist
        elif val == "right":
            self.anglea = -self.twist
        elif val == "off":
            self.anglea = 0

    def setthrust(self, val):
        if val == "on":
            self.thrust = self.maxt
        elif val=="off":
            self.thrust = 0


class Planet(Matter):
    def __init__(self, size, m, x, v=np.zeros(2), anglev=0):
        super().__init__(size, m, x, v, anglev=anglev)
        self.type = "planet"

    def copy(self):
        """returns a copy of this planet"""
        return Planet(self.view, size=self.size, m=self.m,
                      x=copy.copy(self.x), v=copy.copy(self.v))

    def create_image(self):
        """creates a unique polygon image by defining a list of angles"""
        return math.pi*2*sort(np.random.rand(8))


class Level:
    """Controls flow. Needs updating"""
    def __init__(self, root, width = 1000, height=700, interval=0.03):
        w = tk.Canvas(root, width=width, height=height, bg="#444444")
        w.pack()
        self.view = Draw(w, width, height)
        w.focus_set()
        w.bind("<KeyPress-Up>", lambda event: self.player1.setthrust("on"))
        w.bind("<Left>", lambda event: self.player1.settwist("left"))
        w.bind("<Right>", lambda event: self.player1.settwist("right"))
        w.bind("<KeyPress-Down>", lambda event: self.fire(self.player1))
        w.bind("<KeyRelease-Up>", lambda event: self.player1.setthrust("off"))
        w.bind("<KeyRelease-Left>", lambda event: self.player1.settwist("off"))
        w.bind("<KeyRelease-Right>", lambda event: self.player1.settwist("off"))

        w.bind("<KeyPress-w>", lambda event: self.player2.setthrust("on"))
        w.bind("a", lambda event: self.player2.settwist("left"))
        w.bind("d", lambda event: self.player2.settwist("right"))
        w.bind("<KeyPress-s>", lambda event: self.fire(self.player2))
        w.bind("<KeyRelease-w>", lambda event: self.player2.setthrust("off"))
        w.bind("<KeyRelease-a>", lambda event: self.player2.settwist("off"))
        w.bind("<KeyRelease-d>", lambda event: self.player2.settwist("off"))
        w.bind("<space>", lambda event: self.toggle_pause())
        w.bind("r", lambda event: self.start())
        self.timer_interval_ms = int(interval * 1000)
        self.root = root
        self.paused = True
        self.traces = []
        self.objects = []
        self.collision = True
        self.start()

    def start(self):
        """starts a simulation"""
        self.paused = True
        for obj in self.objects:
            self.view.delete(obj)
        asteroid = Rock(size=5, m=1, x=np.array([300, 300.0]),
                      v=np.array([-0.5, 0.2]))
        earth = Planet(size=50, m=200, x=np.array([-100, 0.0]),
                       v=np.array([0, -0.3]), anglev=0.0006)
        moon = Planet(size=30, m=100, x=np.array([300, 0.0]),
                      v=np.array([0, 0.6]))
        player1 = Rocket(m=1, x=np.array([-42.0, 0]),
                         v=np.array([0, 0.9]), landed_on=earth)
        player2 = Rocket(m=1, x=np.array([-100.0, 58]), v=np.array([0, 0.9]),
                        angle=1.5, landed_on=earth, color="lightgreen")
        self.objects = [player1, player2, earth, moon, asteroid]
        self.planets = [earth, moon]
        self.player1 = player1
        self.player2 = player2
        self.home = earth
        self.change_view()
        for obj in self.objects:
            self.view.draw(obj)
            print(obj.v)

    def fire(self, shooter):
        bullet = shooter.fire()
        if bullet != None:
            self.objects.append(bullet)

    def crashed(self, rocket):
        rocket.landing(self.home, random.random()*math.pi)

    def print_momentum(self):
        momentum = np.zeros(2)
        for obj in self.objects:
            if obj.type == "planet":
                print(obj.v)
                momentum += obj.m*obj.v
        print(momentum)

    def center_m(self):
        return sum([obj.m*obj.x for obj in self.objects if obj.type=="planet"])\
               /sum([obj.m for obj in self.objects if obj.type=="planet"])

    def change_view(self):
        """optional view adjustment"""
        self.view.set_center(self.center_m())

    def timer(self):
        """updates model and images"""
        if not self.paused:
            for item in self.objects:
                item.interaction(self.objects, self)
            self.change_view()
            for item in self.objects + self.traces:
                item.update(t=1)
                self.view.draw(item)
            #self.create_trace([self.player1], i)
            self.root.after(self.timer_interval_ms, self.timer)

    def toggle_pause(self):
        """Starts or shuts down the the timer function"""
        #self.print_momentum()
        self.paused = not self.paused
        if not self.paused:
            self.timer()

    def create_trace(self, objects, i):
        """creates a number of trace marks showing the free-fall path
        of the objects, given that i has a certain value. Very slow"""
        if i%30 != 0: return
        self.collision = False
        for trace in self.traces:
            trace.delete()
        self.traces = []
        traced = [k.copy() for k in set(objects + self.planets)]
        planets = [k for k in traced if k.type=="planet"]
        objects = set(planets + traced)
        for i in range(60):
            for item in objects:
                item.interaction(planets, self)
            for item in objects:
                item.update(t=1)
            if i%6 == 0:
                for item in traced:
                    self.traces.append(Trace_mark(self.view, copy.copy(item.x)))
        self.collision = True

class Draw:
    """contains canvas, display functions and shape info"""
    def __init__(self, canvas, width, height):
        self.w = canvas
        self.center = np.array([0, 0])
        self.screencenter = np.array([width/2, -height/2])
        self.zoom = 1

    def set_center(self, center):
        self.center = center

    def set_zoom(self, zoom):
        self.zoom = zoom

    def translate(self, coords):
        """translates a list of simulation coordinates
        to screen coordinates"""
        new = []
        for x in coords:
            x = self.zoom*(x - self.center) + self.screencenter
            new.append([x[0], -x[1]])
        return new

    def polygon(self, id, center, angle, coords, outline="yellow", fill=""):
        """updates the position of the polygon. Coords should be a list of
        (radius, angle) pairs"""
        cartesian = [center + to_cartesian(x[0], x[1] + angle) for x in coords]
        x = self.translate(cartesian)
        if len(coords) == 3:
            a, b, c, d, e, f = x[0][0], x[0][1], x[1][0], x[1][1], x[2][0], x[2][1]
            if id == None:
                id = self.w.create_polygon(a, b, c, d, e, f,
                                           outline=outline, fill=fill)
            else:
                self.w.coords(id, a, b, c, d, e, f)
        return id

    def circle(self, id, center, radius, outline="yellow", fill=""):
        """updates the position of the circle"""
        center = self.translate([center])[0]
        size = radius*self.zoom
        x0, y0 = center[0] -size, center[1] -size
        x1, y1 = center[0] + size + 1, center[1] + size + 1
        if id == None:
            id = self.w.create_oval(x0, y0, x1, y1, outline=outline, fill=fill)
        else:
            self.w.coords(id, x0, y0, x1, y1)
        return id

    def delete(self, obj):
        self.w.delete(obj.id)
        if obj.type=="rocket":
            self.w.delete(obj.thrustid)

    def draw(self, object):
        """Update image of object and returns image tkinter id"""
        if object.type =="rocket":
            self.draw_rocket(object)
        elif object.type == "planet":
            self.draw_planet(object)
        elif object.type == "trace_mark":
            self.draw_trace(object)
        elif object.type == "rock":
            self.draw_planet(object)

    def draw_trace(self, object):
        object.id = self.circle(object.id, object.x,
                                object.size, outline="#5555ff")

    def draw_rocket(self, rocket):
        coords = [[15, 0],[10, math.pi*0.8],[10, -math.pi*0.8]]
        rocket.id = self.polygon(rocket.id, rocket.x, rocket.angle,
                                 coords, outline=rocket.color)
        if rocket.thrust != 0 or rocket.thrustid != None:
            rocket.thrustid = self.draw_thrust(rocket)


    def draw_thrust(self, rocket):
        if rocket.thrust == 0:
            self.w.delete(rocket.thrustid)
            return None
        coords = [[10, math.pi],[18, 0.96*math.pi],[18, -0.96*math.pi]]
        id = self.polygon(rocket.thrustid, rocket.x, rocket.angle,
                          coords, outline="red")
        return id

    def draw_planet(self, planet):
        center = planet.x
        radius = planet.size
        planet.id = self.circle(planet.id, center, radius, outline=planet.color)


def main():
    root = tk.Tk()
    Level(root)
    print("Entering mainloop...")
    tk.mainloop()

if __name__=="__main__":
    main()
