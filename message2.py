# This displays a simple message window
# when function "foo" is called.
# Typically this is imported by another module.


from tkinter import messagebox


def Info(msg):
    messagebox.showinfo('Information', msg)
