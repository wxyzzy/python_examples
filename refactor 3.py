# This is an example of Tkinter

import tkinter


class Hello:
    def __init__(self):
        self.w = tkinter.Tk()
        self.w.title("code example")
        self.w.geometry("450x200")

    def make_contents(self):
        self.l = tkinter.Label(self.w, text="Hello, tkinter!", font=("Courier", 20))
        self.l.grid(padx=100, pady=80)

    def show_window(self):
        self.w.mainloop()



def main():
    w = Hello()
    w.make_contents()
    w.show_window()
    
main()
