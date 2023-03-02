
import tkinter as tk
import message3 as msg


class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text='Open new window',
                                 width=25, command=self.new_window)
        self.button1.pack()
        self.frame.pack()

    def new_window(self):
        self.app = msg.Message(self.master, 'Hello Xxyzzy, this is a slightly longer text. ' +
                               'Ok, it is a very long text to test wrap around.')

        self.app = msg.Message(None, 'Hello Xxyzzy, this is a second window called without a master. ' +
                               'Ok, it is a very long text to test wrap around.')


def main():
    master = tk.Tk()
    Demo1(master)
    master.mainloop()
    msg.message2('We are done.')


if __name__ == '__main__':
    main()
