# ordel helper
#


import tkinter as tk

def main():
    window = tk.Tk()
    window.title("ordel helper")
    window.geometry("820x400")
    
    # selection, 5 characters by 6 attempts
    frame1 = tk.Frame(window, height=300, width=200, bg="#555")
    frame1.grid(row=1, column=1, padx=4, pady=4)
    lbl = []
    for i in range(6):
        for j in range(5):
            a = (tk.Label(frame1, bg='#000', fg='#ffa', width=4, height=2, padx=0, pady=0, 
                          font=('calibre', 12, 'bold'), text=str(j), justify=tk.CENTER))
            a.grid(row=j, column=i, padx=2, pady=2)
            lbl.append(a)
    
    # keyboard
    frame2 = tk.Frame(window, height=300, width=450, bg="#555")
    frame2.grid(row=1, column=2, padx=4, pady=4)
    lbl = []
    for i in range(3):
        for j in range(11):
            index = j + i * 11
            keys = 'qwertyuiopåasdfghjklöäzxcvbnm'
            if index < len(keys):
                ch = keys[index]
                a = (tk.Label(frame2, bg='#000', fg='#ffa', width=4, height=2, padx=0, pady=0,
                              font=('calibre', 12, 'bold'), text=ch, justify=tk.CENTER))
                a.grid(row=i, column=j, padx=2, pady=2)
                lbl.append(a)

    btn = tk.Button(window, text="Spela", command=play)
    btn.grid(row=2, column=1)
    
    # hint
    frame3 = tk.Frame(window, height=100, width=450, bg="#555")
    frame3.grid(row=3, column=1, padx=4, pady=4, columnspan=2)
    text = 'hint - words found: 0'
    a = tk.Label(frame3, bg='#000', fg='#ffa', width=100, height=2, padx=2, pady=2, text=text, justify=tk.CENTER)
    a.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
    text = '[]'
    a = tk.Label(frame3, bg='#000', fg='#ffa', width=100, height=2, padx=2, pady=2, text=text, justify=tk.CENTER)
    a.grid(row=2, column=0, padx=2, pady=2, sticky=tk.W)
    window.bind_all('<Key>', key)
    window.mainloop()

def play():
    pass

def use_char():
    pass

def key(event):
    if event.char == event.keysym:
        msg = 'Normal Key %r' % event.char
    elif len(event.char) == 1:
        msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
    else:
        msg = 'Special Key %r' % event.keysym
    label1.config(text=msg)
    use_char(event.char)
    
main()