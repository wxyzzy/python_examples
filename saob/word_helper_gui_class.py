# ordel helper
# Copyright 2023 James Nash. Licensed under the MIT license.


import tkinter as tk
from tkinter import messagebox
from functools import partial
from form import query_form, query_result


import word_helper_class as wh
wh = wh.Klass()

# In frame1 the current row and char index is:

#button in the selection area

class Klass:
    def __init__(self):
        self.char_index = 0
        self.row_index = 0
        self.window = None
        self.lbl = []
        self.label_color = []
        self.label_char = []
        self.keyboard = []
        self.keys = 'qwertyuiopåasdfghjklöäzxcvbnm'
        self.undefined_color = '#444'
        self.exclude_color = '#000'
        self.required_color = '#608'
        self.pattern_color = '#3a3'
        self.pattern = '_____'
        self.required = ''
        self.excluded = ''
        self.n_label = None
        self.word_label = None
        self.scale = None
        self.text_ = None
        self.key_focus = True
        self.target = ''

    def main(self):
        self.window = tk.Tk()
        self.window.title("ordel helper")
        self.window.geometry("820x550")
        self.window.configure(bg='#555')

            # selection, 5 characters by 6 attempts
        frame1 = tk.Frame(self.window, height=300, width=200, bg="#555")
        frame1.grid(row=1, column=1, padx=4, pady=4)
        self.lbl = []
        for i in range(6):
            for j in range(5):
                index = j + i * 5
                foo = partial(self.color_selection, index)
                a = (tk.Button(frame1, bg=self.undefined_color, fg='#ffa', highlightcolor=self.undefined_color,
                               width=4, height=2, activebackground=self.undefined_color,
                               font=('calibre', 12, 'bold'), justify=tk.CENTER, command=foo))
                a.grid(row=i, column=j, padx=2, pady=2)
                self.lbl.append(a)
                self.label_color.append(self.undefined_color)
                self.label_char.append('')

            # keyboard
        frame2 = tk.Frame(self.window, height=300, width=450, bg="#555")
        frame2.grid(row=1, column=2, padx=4, pady=4)
        for i in range(3):
            for j in range(11):
                index = j + i * 11
                if index < len(self.keys):
                    ch = self.keys[index]
                    a = (tk.Label(frame2, bg=self.undefined_color, fg='#ffa', width=4, height=2, padx=0, pady=0,
                                  font=('calibre', 12, 'bold'), text=ch, justify=tk.CENTER, relief=tk.RAISED))
                    a.grid(row=i, column=j, padx=2, pady=2)
                    self.keyboard.append(a)

            # actions
        frame3 = tk.Frame(self.window, height=100, width=450, bg="#555")
        frame3.grid(row=2, column=1, padx=4, pady=4)
        btn = tk.Button(frame3, text="Restart", bg=self.undefined_color, fg='#ffa', command=self.do_restart)
        btn.grid(row=1, column=1, padx=2)
        btn = tk.Button(frame3, text="Random", bg=self.undefined_color, fg='#ffa', command=self.do_random_word)
        btn.grid(row=1, column=2, padx=2)
        btn = tk.Button(frame3, text="Enter", bg=self.undefined_color, fg='#ffa', command=self.do_enter_word)
        btn.grid(row=1, column=3, padx=2)
        btn = tk.Button(frame3, text="Spela", bg=self.undefined_color, fg='#ffa', command=self.play)
        btn.grid(row=1, column=4, padx=2)

            # hint
        frame4 = tk.Frame(self.window, height=100, width=450, bg="#555")
        frame4.grid(row=3, column=1, padx=4, pady=4, columnspan=2)
        self.text_ = 'hint - words found: 0'
        self.n_label = tk.Label(frame4, bg=self.undefined_color, fg='#ffa', width=100, height=2, padx=2, pady=2, text=self.text_, justify=tk.CENTER)
        self.n_label.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
        self.text_ = '[]'
            #word_label = tk.Label(frame4, bg=undefined_color, fg='#ffa', width=100, height=2, padx=2, pady=2, text=text_, justify=tk.CENTER)
            #word_label.grid(row=2, column=0, padx=2, pady=2, sticky=tk.W)

            # scroll text within word_label
        self.word_label = tk.Text(frame4, bg=self.undefined_color, pady=2, fg='#ffa', width=100, height=5)
        self.word_label.grid(row=2, column=0)
        self.scale = tk.Scrollbar(frame4, bg=self.undefined_color, bd=0, 
                         orient=tk.HORIZONTAL, command=self.word_label.yview)
        self.scale.grid(row=3, column=0, sticky=tk.NSEW)
        self.word_label.config(yscrollcommand=self.scale.set)
        array = 'Ordel Helper (Swedish) may be used beside Ordel.se or Ordel app to help find valid words. \n'
        array += 'Enter the same word used in Ordel.se, click on each letter to change its color, and click on "Play".\n'
        array += 'Or click on "Random" or "Enter" to create a self.target word and self.play Ordel Helper by itself.'
        self.word_label.insert(tk.END, array)

        self.window.bind_all('<Key>', self.key)
        self.window.mainloop()

    def color_selection(self, index):
        b = self.lbl[index]
        if self.label_color[index] == self.undefined_color: self.label_color[index] = self.exclude_color
        elif self.label_color[index] == self.exclude_color: self.label_color[index] = self.required_color
        elif self.label_color[index] == self.required_color: self.label_color[index] = self.pattern_color
        elif self.label_color[index] == self.pattern_color: self.label_color[index] = self.undefined_color
        b.config(bg = self.label_color[index])

            # select row and column
        self.row_index = index // 5
        self.char_index = index % 5
        return

    def do_restart(self):
        self.char_index = 0
        self.row_index = 0
        self.label_color = [self.undefined_color for x in self.label_color]
        self.label_char = ['' for x in self.label_color]
        for l in self.lbl:
            l.config(bg=self.undefined_color, text='')
        for k in self.keyboard:
            k.config(bg=self.undefined_color)
        self.pattern = '_____'
        self.required = ''
        self.excluded = ''
        self.target = ''

    def do_random_word(self):
        ok = messagebox.askokcancel('Random word', 'Select random word from dictionary')
        if ok:
            self.target = wh.get_random_word(5)
            print(self.target)
        return

    def do_enter_word(self):
        self.key_focus = False
        d = {'5 letter self.target word': '', 'callback': self.enter_word_cb}
        query_form(d)
            # results gotten asynchrously using query_result()

    def enter_word_cb(self, d):
        self.key_focus = True
        values = list(d.values())
        self.target = values[0]
        print('self.target: ', self.target)

    def do_scale(self, event):
        index = self.scale.get()
        self.word_label.config()

    def play(self):
            # process target word if defined
        if self.target:
            word = self.label_char[self.row_index * 5: self.row_index * 5 + 5]
            for i, w in enumerate(word):
                j = self.row_index * 5 + i
                if w == self.target[i]:
                    self.label_color[j] = self.pattern_color
                    self.lbl[j].config(bg = self.label_color[j])
                elif w in self.target:
                    self.label_color[j] = self.required_color
                    self.lbl[j].config(bg = self.label_color[j])
                else:
                    self.label_color[j] = self.exclude_color
                    self.lbl[j].config(bg = self.label_color[j])

            # collect information
        self.pattern = ''
        self.required = ''
        self.excluded = ''
        for i in range(self.row_index * 5, self.row_index * 5 + 5):
            self.pattern += self.label_char[i] if self.label_color[i] == self.pattern_color else '_'
        for i in range(self.row_index + 1):
                    # 'required' can look like '____r,__r__' to show where r cannot be
            if i != 0:
                self.required += ','
            for j in range(5):
                k = i * 5 + j
                self.excluded += self.label_char[k] if self.label_color[k] == self.exclude_color else ''
                self.required += self.label_char[k] if self.label_color[k] == self.required_color else '_'

            # remove excluded if ´´ ordel reports a second copy of letter as missing
        for r in self.required:
            if r != '_' and r in self.excluded:
                self.excluded = ''.join([x for x in self.excluded if r != x])
        for p in self.pattern:
            if p != '_' and p in self.excluded:
                self.excluded = ''.join([x for x in self.excluded if p != x])

            # compose query
            # 'ordel -i 5 -p __ta_ -r u -e ee -z
        r = f'-r {self.required}' if self.required else ''
        e = f'-e {self.excluded}' if self.excluded else ''
        query = (f'ordel -i 5 -p {self.pattern} {r} {e} -z')
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
        self.n_label.config(text=str(n))
        array = f'[{s}]'
        self.word_label.delete("1.0", tk.END)
        self.word_label.insert("1.0", array)

            # modify keyboard colors
        for i in range(self.row_index * 5, self.row_index * 5 + 5):
            ch = self.label_char[i]
            color = self.label_color[i]
            if ch in self.keys:
                index = self.keys.find(ch)
                self.keyboard[index].config(bg = color)

            # increment row
        if self.row_index < 5:
            self.row_index += 1
            self.char_index = 0
        return

    def use_char(self, ch):
        if ch == '\r':
            self.play()
        elif (self.char_index < 5 and self.row_index < 6 and ch in 'qwertyuiopåasdfghjklöäzxcvbnm'):
            index = self.char_index + self.row_index * 5
            self.lbl[index].config(text=ch)
            self.label_char[index] = ch
            self.char_index += 1
        elif ch in 'BS' and self.char_index > 0:
            self.char_index -= 1
            index = self.char_index + self.row_index * 5
            self.lbl[index].config(text='')


    def key(self, event):
        if not self.key_focus:
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
        self.use_char(ch)

k = Klass()
k.main()
