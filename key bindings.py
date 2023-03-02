# This is an example of Tkinter
# This binds all key-down events to one function

from tkinter import *

#w, h = 480, 300   # dimension for Swedish flag

window = Tk()
window.geometry("500x350")
prompt = '       Press a key       '
label1 = Label(window, text=prompt, bg='#ffa')
label1.pack()


def key(event):
    if event.char == event.keysym:
        msg = 'Normal Key %r' % event.char
    elif len(event.char) == 1:
        msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
    else:
        msg = 'Special Key %r' % event.keysym
    label1.config(text=msg)


window.bind_all('<Key>', key)
window.mainloop()
