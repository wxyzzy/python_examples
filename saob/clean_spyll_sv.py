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

def analyze_word(d, code):
    # parse word against aff file
    code1 = code.split(' ')
    d.update({'code': code1})
    return d
    
def make_definite_dict():
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
        if any([str(i) in w for i in range(10)]):
            continue
        if any([x in w for x in '-:.,/!']):
            continue
        if len([x for x in w if x.isupper()]):
            continue        if len(s) >= 2:
            w = s[0]
            code = s[1]
            d = {'word': w}
            d = analyze_word(d, code)
            code1 = code.split()
            key = code1[0]
            isnown = [ch for ch in key if ch in 'BDEHY']
            if any(isnown):
                d.update({'part': 'nown'})
            pprint(d)

if __name__ == "__main__":
    if False:
        out = convert_to_dict()
        d1 = '\n'.join(out)
        with open('sv_SE.txt', 'w', encoding='utf-8') as fout:
            fout.write(d1)
    make_definite_dict()    
    print('done')
    