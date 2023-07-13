import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# create the list window
def list_window(the_list, title, completion):
    window = tk.Toplevel()
    window.title(title)
    var = tk.Variable(value=the_list)
    listbox = tk.Listbox(window, listvariable=var,
        height=6, selectmode=tk.EXTENDED)
    listbox.pack(expand=True, fill=tk.BOTH)

    def items_selected(event):
        # get all selected indices
        selected_indices = listbox.curselection()
        # get selected items
        selected_langs = ",".join([listbox.get(i) for i in selected_indices])
        msg = f'You selected: {selected_langs}'
        showinfo(title='Information', message=msg)

    listbox.bind('<<ListboxSelect>>', items_selected)

if __name__ == "__main__":
    def get_result(values):
        print(values)
    def call_list_window():
        my_list = ('fish', 'cat', 'dog')
        list_window(my_list, 'select', get_result)
	    
    root = tk.Tk()
    b = tk.Button(root, text='test list window', command=call_list_window)
    b.pack()
    root.mainloop()
	