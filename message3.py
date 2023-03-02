# This displays a simple message window
# when function "message" is called.
# Typically this is imported by another module.


import tkinter as tk


class Message:
    def __init__(self, master, msg):
        if master is None:
            self.window = tk.Tk()   # new window (independent of master)
        elif True:
            # new window (closes with master)
            self.window = tk.Toplevel(master)
        else:
            self.window = master    # text written in master window
        self.window.title("Information")
        self.window.geometry("400x100")
        self.frame = tk.Frame(self.window)
        lbl = tk.Label(self.frame, text=msg, wraplength=350, justify=tk.LEFT)
        lbl.grid(padx=10, pady=10)
        self.frame.pack()

    def mainloop(self):
        self.window.mainloop()


def message2(msg):
    # this may be called from another file
    m = Message(None, msg)
    m.mainloop()
