# -*- coding: utf-8 -*-
# convert sv_SE.dic to spyll.txt (dictionary)

from pprint import pprint


def convert_to_dict():
    with open('sv_SE.dic', 'r', encoding='utf-8') as f:
        d = f.read()
    out = []
    d1 = d.split('\n')
    for word in d1:
        s = word.split('/')
        w = s[0]
        if any([str(i) in w for i in range(10)]):
            continue
        if any([x in w for x in '-:.,/!']):
            continue
        if len([x for x in w if x.isupper()]):
            continue
        if w:
            out.append(w)
        return out

aff = None

def make_plural(w, code):
    key = code[0]
    plural = None
    if 'G' in key:
        if w[-1] in 'a':
            plural = w[:-1] + 'or'
        elif w[-1] in 'e':
            plural = w[:-1] + 'ar'
        else:
            plural = w[:-1] + 'ar'
    return plural

def make_plural_definite(w, code):
    key = code[0]
    plural_definite = None
    if 'G' in key:
        if w[-1] in 'a':
            plural_definite = w[:-1] + 'orna'
        elif w[-1] in 'e':
            plural_definite = w[:-1] + 'arna'
        else:
            plural_definite = w[:-1] + 'arna' 
    return plural_definite

def make_definite(w, code):
    # form definite tense
    definite = None
    key = code[0]
    if 'C' in key:
        if w[-1] in 'aeiouyåäöé':
            definite = w + 't'
        elif w[-2:] == 'el':
            definite = w + 'let'
        elif w[-2:] == 'er':
            definite = w + 'ret'
        elif w[-1:] == 'm':
            definite = w + 'met'
        elif w[-2:] == 'en':
            definite = w + 'net'
        elif w[-1:] == 'n':
            definite = w + 'net'
    elif 'D' in key:
        if w[-1:] == 'a':
            definite = w + 'nde'
        else:
            definite = w + 'en'
    elif 'E' in key:
        if w[-2:] == 'um':
            definite = w + 'a'
        else:
            definite = w + 'n'
    elif 'F' in key:
        if w[-2:] == 'er':
            definite = w + 'ren'
        if w[-2:] == 'el':
            definite = w + 'len'
        if w[-2:] == 'en':
            definite = w + 'nen'
        if w[-1:] == 'n':
            definite = w + 'nen'
        if w[-1:] == 'm':
            definite = w + 'men'
        if w[-1:] == 'a':
            definite = w + 'ndena'
        if w[-1:] in 'eioä':
            definite = w + 'na'
        else:
            definite = None
    else:
        definite = None
    if definite:
        #print(f'{w}\t{definite}')
        pass
    return definite
    
def make_definite_list(include_all_words = False):
    global aff
    with open('sv_SE.dic', 'r', encoding='utf-8') as f:
        d = f.read()
    with open('sv_SE.aff', 'r', encoding='utf-8') as f:
        aff = f.read()
    out = []
    d1 = d.split('\n')
    for word in d1:
        s = word.split('/')
        w = s[0]
        if w == 'henne':
            print(w)
        if any([str(i) in w for i in range(10)]):
            continue
        if any([x in w for x in '-:.,/!']):
            continue
        if len([x for x in w if x.isupper()]):
            continue        if len(s) >= 2:
            w = s[0]
            code = s[1]
            d = {'word': w}
            code = code.split(' ')
            d.update({'code': code})
            key = code[0]
            can_definite_form  = [ch for ch in key if ch in 'CDEF']
            can_plural_form = [ch for ch in key if ch in 'G']
            if include_all_words:
                out.append(w)            
            if any(can_definite_form):
                d.update({'part': 'nown'})
                definite = make_definite(w, code)
                if definite:
                    d.update({'definite': definite})
                    out.append(definite)
            if any(can_plural_form):
                plural = make_plural(w, code)
                plural_definite = make_plural_definite(w, code)
                if plural:
                    d:update({'plural': plural})
                    out.append(plural)
                if plural_definite:
                    d:update({'plural_definite': plural_definite})
                    out.append(plural_definite)
    return out

if __name__ == "__main__":
    out = make_definite_list(True)
    out1 = '\n'.join([x for x in out if len(x) == 5])
    with open('sv_SE.txt', 'w', encoding='utf-8') as fout:
        fout.write(out1) 
    print('done')
    