# -*- coding: utf-8 -*-
# convert sv_SE.dic and sv_SE.aff to spyll2.txt (dictionary)
# analyses SFX and PFX codes from sv_SE.aff


from pprint import pprint


aff = None
sfxs = None

def conjugate_word(w, code):
    conj = []
    if w[:5] == 'djupa':
        print(w)
    for c in code:
        if c in sfxs:
            sfxs1 = sfxs[c]
            for sfx in sfxs1:
                s, kod, ending, replace, info = sfx
                if c in code and c == kod and ending != 'Y':
                    if '[' in info:
                        end = info.index(']')
                        inside = info[1:end]
                        if inside[0] == '^':
                            ignore = inside[1:]
                            accept = info[end+1:]
                            if w[-1] in ignore + accept:
                                continue
                        else:
                            accept = inside
                    else:
                        accept = info
                    if accept == '':
                        if ending == '0':
                            conj.append(w + replace)
                        elif ending == w[-len(ending):]:
                             conj.append(w[:-len(ending)] + replace)
                    elif w[-len(accept):] == accept:
                        if ending == '0':
                            conj.append(w + replace)
                        elif ending == w[-len(ending):]:
                             conj.append(w[:-len(ending)] + replace)
    return conj
    
def make_word_list():
    global aff, sfxs
    with open('sv_SE.dic', 'r', encoding='utf-8') as f:
        d = f.read()
    with open('sv_SE.aff', 'r', encoding='utf-8') as f:
        aff = f.read()
        aff = aff.split('\n')
    out = []
    d1 = d.split('\n')
    sfxs = [x.replace('  ', ' ').split(' ') for x in aff if x[:3] == 'SFX']
    sfxs = [(x + [' '])[:5] for x in sfxs]
    d = {}
    for kod in 'CDEFGHI':
        value = [x for x in sfxs if x[1] == kod]
        d.update({kod: value})
    sfxs = d
    for word in d1:
        s = word.split('/')
        w = s[0]
        if any([str(i) in w for i in range(10)]):
            continue
        if any([x in w for x in '-:.,/!']):
            continue
        if len([x for x in w if x.isupper()]):
            continue
        w = s[0]
        out.append(w)
        if False and w[:4] == 'afro':
            print(w)        if len(s) >= 2:
            code = s[1]
            code = code.split(' ')[0]
            conj = conjugate_word(w, code)
            out.append(w)                      
            for x in conj:
                out.append(x)
    return out

if __name__ == "__main__":
    out = make_word_list()
    out1 = '\n'.join([x for x in out if len(x) == 5])
    with open('sv_SE2.txt', 'w', encoding='utf-8') as fout:
        fout.write(out1) 
    print('done')
    