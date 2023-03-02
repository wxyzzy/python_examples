# This show the idea of layout with tkinter

import tkinter as tk

window = tk.Tk()
window.title("code example")
window.geometry("450x200")
frame1 = tk.Frame(window, height=300, width=20, bg="#FFA")
frame1.pack()
btn = tk.Button(frame1, text="Button")
btn.pack()
window.mainloop()
