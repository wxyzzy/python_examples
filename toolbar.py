# Radio buttons using images
# https://www.programcreek.com/python/example/7463/Tkinter.Radiobutton


import tkinter as tk


class ToolBar:
    def __init__(self, window):
        self.window = window
        self.frame = tk.Frame(window)
        self.frame.grid()
        self.map = {}
        self.x = 0
        self.selectkey = ''

    def append(self, key, file, selectfile, command):
        img = tk.PhotoImage(file=file, master=self.window)
        selectimg = tk.PhotoImage(file=selectfile, master=self.window)
        b = tk.Button(self.frame, image=img, command=command)
        b.grid(column=0, row=self.x, sticky=tk.W)
        self.map.update({key: {'button': b, 'img': img,
                               'selectimg': selectimg, 'x': self.x}})
        self.x += 1

    def select(self, key):
        if self.selectkey != '':
            b = self.map[self.selectkey]['button']
            img = self.map[self.selectkey]['img']
            b.config(image=img)
        self.selectkey = key
        b = self.map[key]['button']
        selectimg = self.map[key]['selectimg']
        b.config(image=selectimg)


def do_mail():
    bar.select('mail')
    label.config(text='mail')


def do_sheet():
    bar.select('sheet')
    label.config(text='sheet')


def do_doc():
    bar.select('doc')
    label.config(text='doc')

def main():
    global bar, label
    window = tk.Tk()
    window.title("Toolbar")
    window.geometry("500x400")
    
    bar = ToolBar(window)
    bar.append('mail', 'RadioMail.png', 'RadioMailSelect.png', do_mail)
    bar.append('sheet', 'RadioSheet.png', 'RadioSheetSelect.png', do_sheet)
    bar.append('doc', 'RadioDoc.png', 'RadioDocSelect.png', do_doc)
    
    label = tk.Label(window)
    label.grid(column=1, row=0, sticky=tk.N)
    window.mainloop()

if __name__ == "__main__":
    main()
