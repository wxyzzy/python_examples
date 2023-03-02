# This is an example of Tkinter
# Key-event binding to a function

from tkinter import *
from math import *

w, h = 480, 300   # dimension for Swedish flag

window = Tk()
window.geometry("500x350")
prompt = '       Press a key (ex. d, f, g)       '
label1 = Label(window, text=prompt, bg='#ffa')
label1.pack()
c = Canvas(window, width=w, height=h, bg='#af0')
c.pack()


def mk_rect(x0, y0, x1, y1):
    # utility to return a rectangular polygon for tkinter
    x1 += 1
    return (x0, y0, x1, y0, x1, y1, x0, y1, x0, y0)


def smooth_line(canvas, xy, fill, smooth=True):
    x0, y0, x1, y1 = xy
    halffill = int(fill.replace('#', ''), 16) // 2
    halffill = '#' + hex(halffill).replace('0x', '').zfill(3)
    canvas.create_line((x0, y0, x1, y1), fill=halffill, width=2, smooth=True)
    canvas.create_line((x0, y0, x1, y1), fill=fill, width=1, smooth=True)


def draw_something(ch):
    if ch == 'd':
        rect = c.create_polygon(mk_rect(0, 0, w, h),
                                fill='#afa', outline='#afa')
        j = c.create_line((0, 10, 300, 20), fill='red', width=5, smooth=True)
        j = smooth_line(c, (0, 20, 300, 60), fill='#F00', smooth=True)
        j = smooth_line(c, (0, 30, 300, 200), fill='#00F', smooth=True)
    elif ch == 'f':
        rect = c.create_rectangle((0, 0, w, h), fill='blue', outline='blue')
        rect = c.create_rectangle(
            (w*5/16, 0, w*7/16, h), fill='yellow', outline='yellow')
        rect = c.create_rectangle(
            (0, h*4/10, w, h*6/10), fill='yellow', outline='yellow')
    elif ch == 'g':
        rect = c.create_rectangle((0, 0, w, h), fill='#ffd', outline='#ffd')
        first = True
        x1 = x3 = y1 = y3 = 0
        for i in range(8, 100):
            j = i/5
            x10 = x3
            y10 = y3
            x1 = 170 + 170 * sin(j/8)
            y1 = 150 + 150 * cos(j/2)
            x2 = 150 + 140 * sin(j/4)
            y2 = 150 + 100 * cos(j/4)
            x3 = 150 + 140 * sin(j/5)
            y3 = 150 + 100 * cos(j/7)
            if not first:
                j = c.create_line(x10, y10, x1, y1, fill='blue')
                j = c.create_line(x1, y1, x2, y2, fill='green')
                j = c.create_line(x2, y2, x3, y3, fill='red')
            first = False


def key(event):
    if event.char == event.keysym:
        msg = 'Normal Key %r' % event.char
    elif len(event.char) == 1:
        msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
    else:
        msg = 'Special Key %r' % event.keysym
    label1.config(text=msg)
    draw_something(event.char)


window.bind_all('<Key>', key)
window.mainloop()
