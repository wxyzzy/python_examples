# This is an example of Tkinter
# this does shows a button
# when clicked, a new window is displayed,
# and text is shown in the old window


import tkinter as tk
from tkinter import messagebox


window = tk.Tk()
window.title("code example")
window.geometry("400x200")


def helloCallBack():

    w = tk.Label(window, text="Hello, world!", font=("Courier", 20))
    w.pack()    # needed for widgets
    tk.messagebox.showinfo("Hello Tkinter", "This is a messagebox.")


B = tk.Button(window, text="Hello", command=helloCallBack)
B.pack()

window.mainloop()
