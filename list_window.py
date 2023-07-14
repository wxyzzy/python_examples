import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# create the list window
class ListWindow:
    this = None   # work_around
    def __init__(self, the_list, title, completion, multiple=False):
        ListWindow.this = self
        self.completion = completion
        self.multiple = multiple
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.geometry("200x200")
        self.var = tk.Variable(value=the_list)
        self.listbox = tk.Listbox(self.window, listvariable=self.var,
            height=6, selectmode=tk.EXTENDED)
        self.listbox.pack(expand=True, fill=tk.BOTH)
        self.listbox.bind('<<ListboxSelect>>', ListWindow.items_selected)
    
    @staticmethod
    def items_selected(event):
        self = ListWindow.this
        indices = self.listbox.curselection()
        values = [self.listbox.get(i) for i in indices]
        if not self.multiple:
            self.window.destroy()
        self.completion(values)


if __name__ == "__main__":
    def list_window(the_list, title, completion):  
        lw = ListWindow(the_list, title, completion)
    def get_result(values):
        print(values)
    def call_list_window():
        my_list = ('fish', 'cat', 'dog')
        list_window(my_list, 'select', get_result)
	    
    root = tk.Tk()
    root.title('Test list window')
    root.geometry("400x200")
    b = tk.Button(root, text='test list window', command=call_list_window)
    b.pack()
    root.mainloop()
	