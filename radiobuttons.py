# Radio buttons using images
# https://www.programcreek.com/python/example/7463/Tkinter.Radiobutton


import tkinter as tk


window = tk.Tk()
window.title("Radio buttons")
window.geometry("500x400")

app = tk.Frame(window)
app.grid()
app2 = tk.Frame(window)
app2.grid()
imgs = []   # images must persist

tool_mode = tk.IntVar()
tool_mode2 = tk.IntVar()


def tool(frame, tool_mode, x, y, mode, file, command):
    print('tool_mode ', id(tool_mode))
    img = tk.PhotoImage(file=file, master=window)
    imgs.append(img)
    rb = tk.Radiobutton(frame, bg='white', command=command, text=str(mode),
                        image=img, selectimage=img,
                        variable=tool_mode, value=mode, justify=tk.LEFT)
    rb.grid(column=x, row=y, sticky=tk.W)


def refresh():
    mode = tool_mode.get()
    label.config(text='mode selected: ' + str(mode))


tool(app, tool_mode, 0, 1, 1, 'RadioMail.png', refresh)
tool(app, tool_mode, 0, 2, 2, 'RadioSheet.png', refresh)
tool(app, tool_mode, 0, 3, 3, 'RadioDoc.png', refresh)

tool(app2, tool_mode2, 0, 1, 1, 'RadioMail.png', refresh)
tool(app2, tool_mode2, 0, 2, 2, 'RadioSheet.png', refresh)
tool(app2, tool_mode2, 0, 3, 3, 'RadioDoc.png', refresh)

label = tk.Label(app)
label.grid(column=0, row=4)
window.mainloop()
