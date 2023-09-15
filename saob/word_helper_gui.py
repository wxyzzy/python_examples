# ordel helper
# Copyright 2023 James Nash. Licensed under the MIT license.


import tkinter as tk
from tkinter import messagebox
from functools import partial
from form import query_form, query_result

import word_helper as wh
#wh = wh.Klass()


# In frame1 the current row and char index is:
char_index = 0
row_index = 0

#button in the selection area
window = None
lbl = []
label_color = []
label_char = []
keyboard = []
keys = 'qwertyuiopåasdfghjklöäzxcvbnm'
undefined_color = '#444'
exclude_color = '#000'
required_color = '#608'
pattern_color = '#3a3'
pattern = '_____'
required = ''
excluded = ''
n_label = None
word_label = None
scale = None
text_ = None
key_focus = True
target = ''

def main():
    global window, lbl, keyboard, keys, n_label, word_label, scale, text_
    window = tk.Tk()
    window.title("ordel helper")
    window.geometry("820x550")
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
            if index < len(keys):
                ch = keys[index]
                a = (tk.Label(frame2, bg=undefined_color, fg='#ffa', width=4, height=2, padx=0, pady=0,
                              font=('calibre', 12, 'bold'), text=ch, justify=tk.CENTER, relief=tk.RAISED))
                a.grid(row=i, column=j, padx=2, pady=2)
                keyboard.append(a)
    
    # actions
    frame3 = tk.Frame(window, height=100, width=450, bg="#555")
    frame3.grid(row=2, column=1, padx=4, pady=4)
    btn = tk.Button(frame3, text="Restart", bg=undefined_color, fg='#ffa', command=do_restart)
    btn.grid(row=1, column=1, padx=2)
    btn = tk.Button(frame3, text="Random", bg=undefined_color, fg='#ffa', command=do_random_word)
    btn.grid(row=1, column=2, padx=2)
    btn = tk.Button(frame3, text="Enter", bg=undefined_color, fg='#ffa', command=do_enter_word)
    btn.grid(row=1, column=3, padx=2)
    btn = tk.Button(frame3, text="Spela", bg=undefined_color, fg='#ffa', command=play)
    btn.grid(row=1, column=4, padx=2)
    
    # hint
    frame4 = tk.Frame(window, height=100, width=450, bg="#555")
    frame4.grid(row=3, column=1, padx=4, pady=4, columnspan=2)
    text_ = 'words found: 0'
    n_label = tk.Label(frame4, bg=undefined_color, fg='#ffa', width=100, height=2, 
                       padx=2, pady=2, text=text_, justify=tk.CENTER)
    n_label.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
    text_ = '[]'
    #word_label = tk.Label(frame4, bg=undefined_color, fg='#ffa', width=100, height=2, padx=2, pady=2, text=text_, justify=tk.CENTER)
    #word_label.grid(row=2, column=0, padx=2, pady=2, sticky=tk.W)
    
    # scroll text within word_label
    word_label = tk.Text(frame4, bg=undefined_color, pady=2, fg='#ffa', width=100, height=5)
    word_label.grid(row=2, column=0)
    scale = tk.Scrollbar(frame4, bg=undefined_color, bd=0, 
                     orient=tk.HORIZONTAL, command=word_label.yview)
    scale.grid(row=3, column=0, sticky=tk.NSEW)
    word_label.config(yscrollcommand=scale.set)
    array = 'Ordel Helper (Swedish) may be used beside Ordel.se or Ordel app to help find valid words. \n'
    array += 'Enter the same word used in Ordel.se, click on each letter to change its color, and click on "Play".\n'
    array += 'Or click on "Random" or "Enter" to create a target word and play Ordel Helper by itself.'
    word_label.insert(tk.END, array)
    
    window.bind_all('<Key>', key)
    window.mainloop()

def color_selection(index):
    global lbl, label_color, row_index, char_index, key_focus
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

def do_restart():
    global char_index, row_index, lbl, label_color, label_char, word_label
    global pattern, required, excluded, target
    char_index = 0
    row_index = 0
    label_color = [undefined_color for x in label_color]
    label_char = ['' for x in label_color]
    for l in lbl:
        l.config(bg=undefined_color, text='')
    for k in keyboard:
        k.config(bg=undefined_color)
    pattern = '_____'
    required = ''
    excluded = ''
    target = ''
    n_label.config(text='number of words')
    word_label.delete("1.0", tk.END)
    
def do_random_word():
    global target
    ok = messagebox.askokcancel('Random word', 'Select random word from dictionary')
    if ok:
        target = wh.get_random_word(5)
        print(target)
    return

def do_enter_word():
    global key_focus
    key_focus = False
    d = {'5 letter target word': '', 'callback': enter_word_cb}
    query_form(d)
    # results gotten asynchrously using query_result()

def enter_word_cb(d):
    global target, key_focus
    key_focus = True
    values = list(d.values())
    target = values[0]
    print('target: ', target)

def do_scale(event):
    index = scale.get()
    word_label.config()

def play():
    global row_index, char_index, label_char, label_color, target
    global keys, keyboard
    # process target word if defined
    if target:
        word = label_char[row_index * 5: row_index * 5 + 5]
        for i, w in enumerate(word):
            j = row_index * 5 + i
            if w == target[i]:
                label_color[j] = pattern_color
                lbl[j].config(bg = label_color[j])
            elif w in target:
                label_color[j] = required_color
                lbl[j].config(bg = label_color[j])
            else:
                label_color[j] = exclude_color
                lbl[j].config(bg = label_color[j])
    
    # collect information
    pattern = ''
    required = ''
    excluded = ''
    for i in range(row_index * 5, row_index * 5 + 5):
        pattern += label_char[i] if label_color[i] == pattern_color else '_'
    for i in range(row_index + 1):
        # 'required' can look like '____r,__r__' to show where r cannot be
        if i != 0:
            required += ','
        for j in range(5):
            k = i * 5 + j
            excluded += label_char[k] if label_color[k] == exclude_color else ''
            required += label_char[k] if label_color[k] == required_color else '_'
    
    # remove excluded if ´´ ordel reports a second copy of letter as missing
    for r in required:
        if r != '_' and r in excluded:
            excluded = ''.join([x for x in excluded if r != x])
    for p in pattern:
        if p != '_' and p in excluded:
            excluded = ''.join([x for x in excluded if p != x])
        
    # compose query
    # 'ordel -i 5 -p __ta_ -r u -e ee -z
    r = f'-r {required}' if required else ''
    e = f'-e {excluded}' if excluded else ''
    query = (f'ordel -i 5 -p {pattern} {r} {e} -z')
    print('query:  ', query)
    # send query
    n, lst = wh.call(query.split())
    s = ''
    for i, w in enumerate(lst):
        s += w
        if i % 14 == 13:
            s += '\n'
        else:
            s += ', '
    n_label.config(text=str(n))
    array = f'[{s}]'
    word_label.delete("1.0", tk.END)
    word_label.insert("1.0", array)
    
    # modify keyboard colors
    for i in range(row_index * 5, row_index * 5 + 5):
        ch = label_char[i]
        color = label_color[i]
        if ch in keys:
            index = keys.find(ch)
            keyboard[index].config(bg = color)
    
    # increment row
    if row_index < 5:
        row_index += 1
        char_index = 0
    return

def use_char(ch):
    global char_index, row_index, lbl
    if ch == '\r':
        play()
    elif (char_index < 5 and row_index < 6 and ch in 'qwertyuiopåasdfghjklöäzxcvbnm'):
        index = char_index + row_index * 5
        lbl[index].config(text=ch)
        label_char[index] = ch
        char_index += 1
    elif ch in 'BS' and char_index > 0:
        char_index -= 1
        index = char_index + row_index * 5
        lbl[index].config(text='')
        

def key(event):
    global key_focus
    if not key_focus:
        return False
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