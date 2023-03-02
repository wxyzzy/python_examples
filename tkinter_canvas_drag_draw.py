# This is a wonderful example of interactive programming
# author: anonymous


import tkinter
print("Draw by holding down the left mouse button and drag with the mouse")
print("Click on the figures to change color")
window=tkinter.Tk()

canvas = tkinter.Canvas(window, width=750, height=500, bg="gray")
canvas.pack()
musX, musY = 0,0
color = "green"

def take_position(event):
    global musX, musY
    musX = event.x
    musY = event.y
    
def at_click (event):
    take_position(event)

def at_drag (event):
             canvas.create_line(musX, musY, event.x, event.y, fill=color,width=3)
             take_position(event)

              
canvas.bind("<Button-1>", at_click)
canvas.bind("<B1-Motion>", at_drag)
red_id = canvas.create_oval(10, 10, 100, 100, fill="red")
blue_id = canvas.create_oval(400, 10, 200, 200, fill="blue")
green_id = canvas.create_arc(500, 200, 300, 400, fill="green")
yellow_id = canvas.create_rectangle(10, 500, 100, 200, fill="yellow")


def color_red(event):
    global color
    color="red"
def color_blue(event):
    global color
    color = "blue"
def color_green(event):
    global color
    color = "green"
def color_yellow(event):
    global color
    color = "yellow"

canvas.tag_bind(red_id,"<Button-1>", color_red)
canvas.tag_bind(blue_id,"<Button-1>", color_blue)
canvas.tag_bind(green_id,"<Button-1>", color_green)
canvas.tag_bind(yellow_id,"<Button-1>", color_yellow)


    
window.mainloop()
