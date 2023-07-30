# -*- coding: utf-8 -*-
# scripts for ORDEL game

import sys, os, re

data = None
accept_pattern = ''   # gives accept letters and positions (ignore '_')
    # this implies length, as in wordfeud
accept_letters = ''   # gives letters that may be used
    # as in wordfeud
exclude_letters = ''  # exclude letters
    # for example, if all letters may be used except these
required_letters = '' # these letters are required

help = '''
parse [[options] file]
options:
    i - load n letter words or 5 letter if n is missing

This set of scripts starts with (soal.txt) word list.
Option -i removes words that are not used in.
'''

def do_help(argv, i): print(help)

def get_field(argv, i):
    # file name may appear in the i+1 position
    if i+1 >= len(argv): return None
    elif argv[i+1][0] == '-': return None
    else:
        return argv[i+1]
    
def do_init(argv, i):
    pass

def get_word_list(word_length):
    with open('saob.txt', 'r', encoding='utf-8') as f:
        whole = f.read().replace('\r', '').split('\n')
        s = r"^(?:[a-zåäö]{5})$".replace('5', str(word_length))
        pat = re.compile(s)
        words = [w for w in whole if pat.match(w)]
    return words

def do_get_words(argv, i):
    # given word length, load data, load 5 if length is missing
    n = get_field(argv, i)
    n = 5 if n is None else n
    words = get_word_list(n)
    print('number of words: ', len(words))
    global data
    data = words

def do_analysis(argv, i):
    # type of analysis depends on global variables 
    global accept_pattern, accept_letters, exclude_letters
    ap, al, el = accept_pattern, accept_letters, exclude_letters
    rl = required_letters
    n = len(ap)
    allowed = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    allowed += [x for x in 'åäö']
    allowed = al if al else allowed
    allowed = [x for x in allowed if x != (el if el else '')]
    if ap == al == el == '':
        # summarize number of words of various lengths
        print('word_len\tn_found\texample')
        for n in range(1, 40):
            words = get_word_list(n) 
            n_found = len(words)
            print(str(n) + '\t' + str(n_found) + '\t' + ', '.join(words[:5]))
    elif n:
        def test(w):
            nonlocal allowed
            wordfeud = True
            if ap and wordfeud:
                # test various offsets between ap and w so as to include
                # ap, less the required ap with stripped underscore
                # plus the actual non _ characters
                ap1 = ap.rstrip('_').lstrip('_')
                ap2 = [ch for ch in ap1 if ch != '_']
                len1 = len(ap1)
                len2 = len(ap2)
                max_offset = len(allowed) - len(ap1) + len(ap2)
                for offset in range(max_offset):
                    found = True
                    for i, ch in enumerate(w):
                        j = i - offset
                        if j < 0 or j >= len1-1:
                            if ch not in allowed:
                                found = False
                                break
                        elif ap1[j] == '_':
                            if ch not in allowed:
                                found = False
                                break
                        elif ch != ap1[j]:
                            found = False
                            break
                    if found:
                        return True
                return False
            elif ap:
                if len(w) != len(ap):
                    return False
                for i, ch in enumerate(w):
                    if not (ap[i] == '_' and ch in allowed or ap[i] == ch):
                        return False
            else:
                for ch in w:
                    if ch not in allowed:
                        return False
            if rl:
                for ch in rl:
                    if ch not in w:
                        return False
            return True
        words = get_word_list(n)
        words = [w for w in words if test(w)]
        n_found = len(words)
        print('words_found: ', n_found)
        
        
def do_accept_pattern(argv, i):
    x = get_field(argv, i)
    global accept_pattern
    accept_pattern = x
    
def do_accept_letters(argv, i):
    x = get_field(argv, i)
    global accept_letters
    accept_letters = x
    
def do_exclude_letters(argv, i):
    x = get_field(argv, i)
    global exclude_letters
    exclude_letters = x
    
def do_required_letters(argv, i):
    x = get_field(argv, i)
    global required_letters
    required_letters = x
    
def action(argv, opts):
    # do something for various '-' options
    switch = {'h':do_help, 'i':do_get_words, 'p':do_accept_pattern,
              'a':do_accept_letters, 'e':do_exclude_letters, 
              'r':do_required_letters, 'z':do_analysis}
    for ch, i in opts:
        if ch in switch:
            switch[ch](argv, i)
            
def parse_options(argv):
    # option and position i is saved in opts
    # i is saved to optionally get_filename in position i+1
    opts = []
    for i, arg in enumerate(argv):
        if arg[0] == '-':
            opts.extend([(ch, i) for ch in arg[1:]])
    return opts

def main(argv):
    # parse for '-' options
    n = len(argv)
    if n <= 1:
        # example from wordfeud where given pattern and allowed
        argv = [argv[0]] + '-p _a_i__ -a wrranex -z'.split()
    opts = parse_options(argv)
    action(argv, opts)
    
if __name__ == "__main__":
    main(sys.argv)
    