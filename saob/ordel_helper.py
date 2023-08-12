# ordel helper
#


import tkinter as tk
import word_helper as wh
from functools import partial


# In frame1 the current row and char index is:
char_index = 0
row_index = 0

#button in the selection area
lbl = []
label_color = []
label_char = []
undefined_color = '#333'
exclude_color = '#000'
required_color = '#088'
pattern_color = '#3a3'
pattern = '_____'
required = ''
excluded = ''
n_label = None
word_label = None

def main():
    global lbl, n_label, word_label
    window = tk.Tk()
    window.title("ordel helper")
    window.geometry("820x450")
    window.configure(bg='#555')
    
    # selection, 5 characters by 6 attempts
    frame1 = tk.Frame(window, height=300, width=200, bg="#555")
    frame1.grid(row=1, column=1, padx=4, pady=4)
    lbl = []
    for i in range(6):
        for j in range(5):
            index = j + i * 5
            foo = partial(color_selection, index)
            a = (tk.Button(frame1, bg=undefined_color, fg='#ffa', highlightcolor=undefined_color,
                           width=4, height=2, activebackground=undefined_color,
                           font=('calibre', 12, 'bold'), justify=tk.CENTER, command=foo))
            a.grid(row=i, column=j, padx=2, pady=2)
            lbl.append(a)
            label_color.append(undefined_color)
            label_char.append('')
    
    # keyboard
    frame2 = tk.Frame(window, height=300, width=450, bg="#555")
    frame2.grid(row=1, column=2, padx=4, pady=4)
    for i in range(3):
        for j in range(11):
            index = j + i * 11
            keys = 'qwertyuiopåasdfghjklöäzxcvbnm'
            if index < len(keys):
                ch = keys[index]
                a = (tk.Label(frame2, bg=undefined_color, fg='#ffa', width=4, height=2, padx=0, pady=0,
                              font=('calibre', 12, 'bold'), text=ch, justify=tk.CENTER, relief=tk.RAISED))
                a.grid(row=i, column=j, padx=2, pady=2)
                #lbl.append(a)

    btn = tk.Button(window, text="Spela", bg=undefined_color, fg='#ffa', command=play)
    btn.grid(row=2, column=1)
    
    # hint
    frame3 = tk.Frame(window, height=100, width=450, bg="#555")
    frame3.grid(row=3, column=1, padx=4, pady=4, columnspan=2)
    text = 'hint - words found: 0'
    n_label = tk.Label(frame3, bg=undefined_color, fg='#ffa', width=100, height=2, padx=2, pady=2, text=text, justify=tk.CENTER)
    n_label.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
    text = '[]'
    word_label = tk.Label(frame3, bg=undefined_color, fg='#ffa', width=100, height=2, padx=2, pady=2, text=text, justify=tk.CENTER)
    word_label.grid(row=2, column=0, padx=2, pady=2, sticky=tk.W)
    window.bind_all('<Key>', key)
    window.mainloop()

def color_selection(index):
    global lbl, label_color, row_index, char_index
    b = lbl[index]
    if label_color[index] == undefined_color: label_color[index] = exclude_color
    elif label_color[index] == exclude_color: label_color[index] = required_color
    elif label_color[index] == required_color: label_color[index] = pattern_color
    elif label_color[index] == pattern_color: label_color[index] = undefined_color
    b.config(bg = label_color[index])
    
    # select row and column
    row_index = index // 5
    char_index = index % 5    
    return

def play():
    global row_index
    # collect information
    # for now, assume first row only
    pattern = ''
    required = ''
    excluded = ''
    for i in range(row_index * 5, row_index * 5 + 5):
        pattern += label_char[i] if label_color[i] == pattern_color else '_'
        required += label_char[i] if label_color[i] == required_color else ''
    for i in range(row_index * 5 + 5):
        excluded += label_char[i] if label_color[i] == exclude_color else ''
    
    # compose query
    # 'ordel -i 5 -p __ta_ -r u -e ee -z
    r = f'-r {required}' if required else ''
    e = f'-e {excluded}' if excluded else ''
    query = (f'ordel -i 5 -p {pattern} {r} {e} -z')
    
    # send query
    n, lst = wh.call(query.split()) 
    s = ',  '.join(lst[:20])
    n_label.config(text=str(n))
    word_label.config(text=f'[{s}]')
    return

def use_char(ch):
    global char_index, row_index, lbl
    if ch == '\r':
        play()
    elif (char_index < 5 and row_index < 6 and
        ch in 'qwertyuiopåasdfghjklöäzxcvbnm'):
        index = char_index + row_index * 5
        lbl[index].config(text=ch)
        label_char[index] = ch
        char_index += 1
    elif ch in 'BS' and char_index > 0:
        char_index -= 1
        index = char_index + row_index * 5
        lbl[index].config(text='')
        

def key(event):
    if event.char == event.keysym:
        msg = 'Normal Key %r' % event.char
        ch = event.char
    elif event.char in 'åäö\r':
        ch = event.char
    elif len(event.char) == 1:
        msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
        ch = 'BS'
    else:
        msg = 'Special Key %r' % event.keysym
        ch = ''
    #label1.config(text=msg)
    use_char(ch)
    
main()