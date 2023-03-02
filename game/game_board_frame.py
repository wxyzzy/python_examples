# example of drag
# https://stackoverflow.com/questions/37280004/tkinter-how-to-drag-and-drop-widgets


import tkinter as tk
from PIL import Image, ImageTk
from math import sqrt

w_width, w_height = 400, 400
imgs = []    # required so that images persist

def add_image(frame, filename):
    global imgs, widgets
    img0 = Image.open(filename)
    img_max = max(img0.size)
    img_size = tuple(x * 70 // img_max for x in img0.size)
    img = ImageTk.PhotoImage(img0.resize(img_size, Image.ANTIALIAS))
    imgs.append(img)
    widget = tk.Label(frame, image = img)
    w, h = tuple(10 + (70 - w) // 2 for w in img_size)
    widget.place(x=w, y=h)
    return widget

def add_canvas(frame, width=88, height=88, bg="#dda"):
    widget = tk.Canvas(frame, width=width, height=height, bg=bg)
    widget.place(x=0, y=0)
    return widget

def make_parent_draggable(widget):
    make_draggable(widget)
    widget.__dict__.update({'parent_gets_event': True})

def who_gets_event(event):
    widget, who = event.widget, 'parent_gets_event'
    return widget.__dict__['master'] if hasattr(widget, who) and getattr(widget, who) else widget

def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)
    widget.bind("<ButtonRelease-1>", on_drag_stop)

def on_drag_start(event):
    widget = who_gets_event(event)
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    widget.tkraise()

def on_drag_motion(event):
    widget = who_gets_event(event)
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

def animate_snap(widget, cx1, cy1, i=20):
    px0, py0 = widget.winfo_x(), widget.winfo_y()
    px1, py1 = px0 + widget.winfo_width(), py0 + widget.winfo_height()
    cx0, cy0 = (px0 + px1) // 2, (py0 + py1) // 2
    dx, dy = cx1 - cx0, cy1 - cy0
    if i > 1 and abs(dx) + abs(dx) > 0:
        sign = lambda x: -1 if x<0 else 1
        dx = round(sign(dx) * sqrt(abs(dx)))
        dy = round(sign(dy) * sqrt(abs(dy)))
        widget.after(5, animate_snap, widget, cx1, cy1, i-1)
    widget.place(x=px0+dx, y=py0+dy)
    a = 1
    
def on_drag_stop(event):
    animate = True
    snap_to_grid = True
    widget = who_gets_event(event)
    px0, py0 = widget.winfo_x(), widget.winfo_y()
    px1, py1 = px0 + widget.winfo_width(), py0 + widget.winfo_height()
    cx0, cy0 = (px0 + px1) // 2, (py0 + py1) // 2
    w, h = 100, 100    # dimensions of board element
    cx1, cy1 = cx0 // w * w + 50, cy0 // h * h + 50
    cx1 = w//2 if cx1 < 0 else w_width-w//2 if cx1 > w_width else cx1
    cy1 = h//2 if cy1 < 0 else w_height-h//2 if cy1 > w_height else cy1
    animate_snap(widget, cx1, cy1)

def main():
        window = tk.Tk()
        window.geometry(f"{w_width}x{w_height}")
        
        from random import randint
        board = []
        for i in range(4): 
            row = []
            for j in range(4):
                ranx = lambda: f"{randint(0, 255):x}".zfill(2)
                frame = tk.Frame(window, bg=f"#{ranx()}{ranx()}{ranx()}", width=100, height=100)
                frame.place(x=100*i, y=100*j)
                make_draggable(frame)
                row.append(frame)
            board.append(row)
        
        frame1 = tk.Frame(window, bd=4, bg="grey", width=100, height=100)
        frame1.place(x=50, y=10)
        filename = "Chess_rlt60.png"
        widget = add_image(frame1, filename)
        make_parent_draggable(widget)
        make_draggable(frame1)
        
        frame2 = tk.Frame(window, bd=4, bg="green", width=100, height=100)
        frame2.place(x=110, y=80)
        make_draggable(frame2)
        canvas = add_canvas(frame2)
        make_parent_draggable(canvas)
        canvas.create_oval(10, 10, 80, 80, outline="#b40", fill="#e50")
        
        window.mainloop()

if __name__ == "__main__":
    main()