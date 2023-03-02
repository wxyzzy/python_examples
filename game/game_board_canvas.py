# example of drag
# https://stackoverflow.com/questions/37280004/tkinter-how-to-drag-and-drop-widgets


import tkinter as tk
from PIL import Image, ImageTk
from math import sqrt

w_width, w_height = 400, 400
imgs = []    # required so that images persist

def center_item(canvas, item, bounds):
    x0, y0, x1, y1 = canvas.bbox(item)
    cx0, cy0, cx1, cy1 = bounds
    offset_x = (cx0 + cx1) // 2 - (x0 + x1) // 2 
    offset_y = (cy0 + cy1) // 2 - (y0 + y1) // 2 
    canvas.move(item, offset_x, offset_y)
    
def add_image(canvas, filename, max_dimension):
    global imgs
    img0 = Image.open(filename)
    img_max = max(img0.size)
    img_size = tuple(x * max_dimension // img_max for x in img0.size)
    img = ImageTk.PhotoImage(img0.resize(img_size, Image.ANTIALIAS))
    imgs.append(img)
    x, y = tuple(10 + (70 - w) // 2 for w in img_size)
    item = canvas.create_image(x, y, anchor=tk.NW, image=img)
    return item

def add_canvas(frame, width=88, height=88, bg="#dda"):
    widget = tk.Canvas(frame, width=width, height=height, bg=bg)
    widget.place(x=0, y=0)
    return widget

def make_draggable(canvas, item):
    canvas.tag_bind(item, "<Button-1>", on_drag_start)
    canvas.tag_bind(item, "<B1-Motion>", on_drag_motion)
    canvas.tag_bind(item, "<ButtonRelease-1>", on_drag_stop)

def on_drag_start(event):
    canvas = event.widget
    item = canvas.find_closest(event.x, event.y)
    canvas._drag_item = item
    canvas._drag_start_x = event.x
    canvas._drag_start_y = event.y
    canvas._drag_last_x = event.x
    canvas._drag_last_y = event.y
    canvas.focus(item)
    canvas.lift(item)

def on_drag_motion(event):
    canvas = event.widget
    #item = canvas.find_closest(event.x, event.y)
    item = canvas._drag_item
    bounds = canvas.bbox(item)
    dx = event.x - canvas._drag_last_x
    dy = event.y - canvas._drag_last_y
    canvas._drag_last_x = event.x
    canvas._drag_last_y = event.y
    canvas.move(item, dx, dy)

def animate_snap(canvas, cx1, cy1, i=20):
    item = canvas._drag_item    
    px0, py0, px1, py1 = canvas.bbox(item)
    cx0, cy0 = (px0 + px1) // 2, (py0 + py1) // 2
    dx, dy = cx1 - cx0, cy1 - cy0
    if i > 1 and abs(dx) + abs(dx) > 0:
        sign = lambda x: -1 if x<0 else 1
        dx = round(sign(dx) * sqrt(abs(dx)))
        dy = round(sign(dy) * sqrt(abs(dy)))
        canvas.after(10, animate_snap, canvas, cx1, cy1, i-1)
    canvas.move(item, dx, dy)
    
def on_drag_stop(event):
    canvas = event.widget
    item = canvas._drag_item
    px0, py0, px1, py1 = canvas.bbox(item)
    cx0, cy0 = (px0 + px1) // 2, (py0 + py1) // 2
    w, h = 100, 100    # dimensions of board element
    cx1, cy1 = cx0 // w * w + 50, cy0 // h * h + 50
    cx1 = w//2 if cx1 < 0 else w_width-w//2 if cx1 > w_width else cx1
    cy1 = h//2 if cy1 < 0 else w_height-h//2 if cy1 > w_height else cy1
    animate_snap(canvas, cx1, cy1)

def main():
    window = tk.Tk()
    window.geometry(f"{w_width}x{w_height}")
    board = add_canvas(window, width=w_width, height=w_height)
    
    from random import randint
    rows = []
    for j in range(4): 
        row = []
        for i in range(4):
            ranx = lambda: f"{randint(0, 255):x}".zfill(2)
            x=100*i; y=100*j
            rec = (x, y, x+100, y+100)
            item = board.create_rectangle(*rec, fill=f"#{ranx()}{ranx()}{ranx()}")
            #make_draggable(board, item)
            row.append(item)
        rows.append(row)
    
    item = board.create_oval(10, 110, 80, 180, outline="#b40", fill="#e50")
    make_draggable(board, item)
    center_item(board, item, board.bbox(5))
    
    filename = "Chess_rlt60.png"
    item = add_image(board, filename, 80)
    center_item(board, item, board.bbox(9))
    make_draggable(board, item)
    window.mainloop()

if __name__ == "__main__":
    main()
