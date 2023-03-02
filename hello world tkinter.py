# This is an example of Tkinter

import tkinter

window = tkinter.Tk()
window.title("code example")
window.geometry("450x200")

w = tkinter.Label(window, text="Hello, tkinter!", font=("Courier", 20))
w.grid(padx=100, pady=80)

window.mainloop()
