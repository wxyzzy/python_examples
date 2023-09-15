# form1 - tkinter form #1
# showing the use of the Entry widget


import tkinter as tk
from functools import partial

n = 0
win = None
outdata = {}

def query_form(indata):
    # indata is a dictionary of key:values
    global n, outdata
    if 'callback' in indata:
        callback = indata.pop('callback')
    else:
        callback = None
    def submit():
        nonlocal indata
        global outdata
        outdata = {}
        k = indata.keys()
        n = len(k)
        for i in range(n):
            outdata.update({label[i]: rcvr[i].get()})
            rcvr[i].set("")
        if callback:
            callback(outdata)
        win.destroy()
    win = tk.Toplevel()
    outdata = {}       # a dictionary {label: value}
    label = list(indata.keys())
    value = list(indata.values())
    rcvr = [tk.StringVar() for x in indata]  # receivers for data
    n = len(rcvr)
    wlabel = []    # label widget
    wentry = []    # text entry widget
    for i in range(n):
        #rcvr[i].set(value[i])
        wlabel.append(tk.Label(win, text=label[i],
                               font=('calibre', 10, 'bold')))
        wentry.append(tk.Entry(win, textvariable=rcvr[i],
                               font=('calibre', 10, 'normal')))
        wlabel[i].grid(row=i, column=0)
        wentry[i].grid(row=i, column=1)
        wentry[i].insert(0, value[i])
    sub_btn = tk.Button(win, text='Submit', command=submit)
    sub_btn.grid(row=n, column=1)
    #win.mainloop()

def query_result():
    global outdata
    return outdata

def main():
    global indata, outdata
    root = tk.Tk()
    d = {'name': '', 'password': '*****', 'phone': '+46-'}
    indata = d
    btn = tk.Button(win, text='Form', command=partial(query_form, indata))
    btn.pack()
    root.mainloop()
    results = outdata
    print(results)


if __name__ == "__main__":
    main()
