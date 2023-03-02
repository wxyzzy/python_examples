# This combines Tkinter and Threading


import tkinter as tk
import threading as thr
import time

thread_count = 0
class WindowHandler:
    def __init__(self):
        self.msg = ''
        self.window = tk.Tk()
        self.window.geometry("500x350")
        prompt = '       Press a key       '
        self.label1 = tk.Label(self.window, text=prompt, bg='#ffa')
        self.label1.pack()
        
    def start(self):
        global thread_count
        thread_count += 1
        self.window.bind_all('<Key>', self.key)
        self.window.mainloop()
        thread_count -= 1
        
    def key(self, event):
        if event.char == event.keysym:
            self.msg = 'Normal Key %r' % event.char
        elif event.char in 'åäö':
            self.msg = 'Swedish char %r' % event.char
        elif len(event.char) == 1:
            self.msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
        else:
            self.msg = 'Special Key %r' % event.keysym
        self.label1.config(text=self.msg)

def main():
    wh1 = WindowHandler()
    wh1.start()

main()
