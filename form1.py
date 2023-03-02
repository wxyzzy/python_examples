# form1 - tkinter form #1
# showing the use of the Entry widget


import tkinter as tk


class Form1:
    def __init__(self, indata):
        self.root = tk.Tk()
        self.indata = indata    # a dictionary {label: value}
        self.outdata = {}       # a dictionary {label: value}
        self.label = list(indata.keys())
        self.value = list(indata.values())
        self.rcvr = [tk.StringVar() for x in indata]  # receivers for data
        self.n = len(self.rcvr)
        self.setup()

    def setup(self):
        self.wlabel = []    # label widget
        self.wentry = []    # text entry widget
        for i in range(self.n):
            self.wlabel.append(tk.Label(self.root, text=self.label[i],
                                        font=('calibre', 10, 'bold')))
            self.wentry.append(tk.Entry(self.root, textvariable=self.rcvr[i],
                                        font=('calibre', 10, 'normal')))
            self.wlabel[i].grid(row=i, column=0)
            self.wentry[i].grid(row=i, column=1)
            self.wentry[i].insert(0, self.value[i])
        self.sub_btn = tk.Button(self.root, text='Submit', command=self.submit)
        self.sub_btn.grid(row=self.n, column=1)

    def submit(self):
        self.outdata = {}
        for i in range(self.n):
            self.outdata.update({self.label[i]: self.wentry[i].get()})
            self.rcvr[i].set("")
        self.root.destroy()

    def getresults(self):
        self.root.mainloop()
        return self.outdata


def main():
    d = {'name': '', 'password': '*****', 'phone': '+46-'}
    form = Form1(d)
    d = form.getresults()
    print(d)


if __name__ == "__main__":
    main()
