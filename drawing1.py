import tkinter as tk

window = tk.Tk()

c = tk.Canvas(window, bg="green", height=250, width=300)
c.pack()

coord = 10, 50, 210, 250
arc = c.create_arc(coord, start=0, extent=130, fill="#F00")
line = c.create_line(10, 10, 200, 200, fill='white')

img = tk.PhotoImage(file = "RadioDoc.png", master=window) 
c.create_image(0, 0, anchor=tk.NW, image=img)

window.mainloop()
