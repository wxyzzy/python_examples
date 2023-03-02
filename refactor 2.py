# This is an example of Tkinter

import tkinter

def get_window():
    w = tkinter.Tk()
    w.title("code example")
    w.geometry("450x200")
    return w

def get_contents(w):
    l = tkinter.Label(w, text="Hello, tkinter!", font=("Courier", 20))
    l.grid(padx=100, pady=80)
    return l

def show_window(w):
    w.mainloop()



def main():
    w = get_window()
    c = get_contents(w)
    show_window(w)
    
main()
