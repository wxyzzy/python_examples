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

def make_definite(w, code):
    # form definite tense
    definite = w
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
            # JKLMNOPQR - verb or adjective
            if any(can_definite_form):
                d.update({'part': 'nown'})
                definite = make_definite(w, code)
                if definite:
                    d.update({'definite': definite})
                    out.append((w, definite))
                elif include_all_words:
                    out.append((w, None))
            elif include_all_words:
                out.append((w, None))
    return out

if __name__ == "__main__":
    out = make_definite_list(True)
    out1 = '\n'.join([w + '\n' + d if d else w for w, d in out])
    with open('sv_SE.txt', 'w', encoding='utf-8') as fout:
        fout.write(out1) 
    print('done')
    