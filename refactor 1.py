# This is an example of Tkinter

import tkinter

w = tkinter.Tk()
w.title("code example")
w.geometry("450x200")

l = tkinter.Label(w, text="Hello, tkinter!", font=("Courier", 20))
l.grid(padx=100, pady=80)

w.mainloop()
