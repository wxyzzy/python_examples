# -*- coding: utf-8 -*-
# scripts for ORDEL game

import sys, os, re


        # this implies length, as in wordfeud
        # as in wordfeud
        # for example, if all letters may be used except these


help = '''
parse [[options] file]
where [options] = [option extra_word]
options (preceded by '-' character):
    i - limit dictionary to n letter words
    a - enter accept letters that are allowed (wordfeud)
    r - enter required letters (wordel), can be a pattern like __r__
    e - enter exclude letters (wordel)
    p - enter accept pattern (including _ for wildcard)
    w - force wordfeud rules on pattern matching (not wordel)
    z - do analysis producing a list of words

This set of scripts starts with (soal.txt) word list.
Option -r may have multiple patterns such as __r__,r___a.
   This removes words with r if in position 0, 2 and a if in position 4
'''

class Klass:
    def __init__(self):
        self.accept_pattern = ''   # gives accept letters and positions (ignore '_')
        self.accept_letters = ''   # gives letters that may be used
        self.exclude_letters = ''  # exclude letters
        self.required_letters = '' # these letters are required
        self.wordfeud = False      # scan accept_pattern using wordfeud rule
        self.words = None

    def do_help(self, argv, i):
        print(help)

    def get_field(self, argv, i):
        # file name may appear in the i+1 position
        if i+1 >= len(argv): return None
        elif argv[i+1][0] == '-': return None
        else:
            return argv[i+1]

    def do_init(self, argv, i):
        pass

    def get_word_list(self, word_length):
        #filename = 'saob.txt'
        #filename = 'sv_SE.txt'
        filename = 'sv_SE2.txt'
        with open(filename, 'r', encoding='utf-8') as f:
            whole = f.read().replace('\r', '').split('\n')
            #print(len(whole))
            if word_length:
                s = r"^([a-zåäö]{5})$".replace('5', str(word_length))
            else:
                s = r"^([a-zåäö]+)$"
            pat = re.compile(s)
            obj.words = [w for w in whole if pat.match(w)]
        return obj.words

    def get_random_word(self, word_length):
        import random
        obj.words = obj.get_word_list(word_length)
        n = len(obj.words)
        i = random.randint(0, n)
        return obj.words[i]

    def do_get_words(self, argv, i):
        # given word length, load words
        n = obj.get_field(argv, i)
        obj.words = obj.get_word_list(n)

    def do_analysis(self, argv, i):
        # type of analysis depends on global variables 
        ap, al, el = obj.accept_pattern, obj.accept_letters, obj.exclude_letters
        rl = obj.required_letters.split(',')
        n = len(ap)
        allowed = [chr(x) for x in range(ord('a'), ord('z') + 1)]
        allowed += [x for x in 'åäö']
        allowed = al if al else allowed
        allowed = [x for x in allowed if x not in (el if el else '')]
        if ap == al == el == '':
            # summarize number of words of various lengths
            print('word_len\tn_found\texample')
            for n in range(1, 40):
                obj.words = obj.get_word_list(n) 
                n_found = len(obj.words)
                print(str(n) + '\t' + str(n_found) + '\t' + ', '.join(obj.words[:5]))
        elif n:
            def test(self, w):
                nonlocal allowed
                if ap and obj.wordfeud:
                    # test various offsets between ap and w so as to include
                    # ap, less the required ap with stripped underscore
                    # plus the actual non _ characters
                    if False and w == 'henne':
                        print(w)
                    ap1 = ap.rstrip('_').lstrip('_')
                    len1 = len(ap1)
                    ap2 = [x for x in ap1 if x != '_']
                    max_offset = len(w) - len1
                    for offset in range(max_offset):
                        # convolve ap1 over w
                        oks = []   # collect ok results for each ap1 character
                        allowed1 = allowed.copy()
                        for i, apx in enumerate(ap1):
                            ok = False
                            if apx == '_':
                                if w[i] in allowed1:
                                    ok = True
                                    # remove wordfeud tile
                                    k = allowed1.index(w[i])
                                    del allowed1[k]
                            else:
                                if apx == w[i+offset]:
                                    ok = True
                            oks.append(ok)
                        if min(oks) == True:
                            allowed1 = allowed + ap2
                            for ch in w:
                                if ch in allowed1:
                                    k = allowed1.index(ch)
                                    del allowed1[k]
                                else:
                                    return False
                            return True
                    return False
                elif ap:
                    if True and w == 'pågår':
                        print(w)
                    if len(w) != len(ap):
                        return False
                    for ch in w:
                        if ch not in allowed:
                            return False
                    for i, ch in enumerate(w):
                        if ap[i] != '_' and ap[i] != ch:
                            return False
                        if ch in obj.exclude_letters:
                            return False
                    for r in rl:
                        for i, ch in enumerate(r):
                            if ch != '_' and ch not in w:
                                return False
                            # rl shows a pattern of where required letters are; 
                            # the letter does not belong in this position
                            if '_' in r and ch != '_' and ch == w[i]:
                                return False
                else:
                    for ch in w:
                        if ch not in allowed:
                            return False
                    for r in rl:
                        for ch in r:
                            if ch not in w:
                                return False
                return True
            #words = get_word_list(n)
            obj.do_get_words(argv, i)
            #print('original words: ', len(words))
            obj.words = [w for w in obj.words if obj.test(w)]
            obj.words = list(set(obj.words))
            obj.words.sort()
            n_found = len(obj.words)
            return n_found, obj.words


    def do_accept_pattern(self, argv, i):
        x = obj.get_field(argv, i)
        obj.accept_pattern = x

    def do_accept_letters(self, argv, i):
        x = obj.get_field(argv, i)
        obj.accept_letters = x

    def do_exclude_letters(self, argv, i):
        x = obj.get_field(argv, i)
        obj.exclude_letters = x

    def do_required_letters(self, argv, i):
        x = obj.get_field(argv, i)
        obj.required_letters = x

    def do_wordfeud(self, argv, i):
        obj.wordfeud = True

    def action(self, argv, opts):
        # do something for various '-' options
        switch = {'h':obj.do_help, 'i':obj.do_get_words, 'p':obj.do_accept_pattern,
                  'a':obj.do_accept_letters, 'e':obj.do_exclude_letters, 
                  'r':obj.do_required_letters, 'w':obj.do_wordfeud, 'z':obj.do_analysis}
        for ch, i in opts:
            if ch in switch:
                result = switch[ch](argv, i)
                if ch == 'z':
                    return result

    def parse_options(self, argv):
        # option and position i is saved in opts
        # i is saved to optionally get_filename in position i+1
        opts = []
        for i, arg in enumerate(argv):
            if arg[0] == '-':
                opts.extend([(ch, i) for ch in arg[1:]])
        return opts

    def call(self, argv):
        # this is the entry point for main programs that call this module
        # argv is a list containing the name of the program, followed by parameters
        # the result is a tuple containing length and word list
        opts = obj.parse_options(argv)
        result = obj.action(argv, opts)
        return result


if __name__ == "__main__":
    obj = Klass()
    def main(argv):
        # parse for '-' options
        n = len(argv)
        if n <= 1:
            # example from obj.wordfeud where given pattern and allowed char is used
            params = '-w -p lla -a slixel -z'
            # example from wordel where word length is 5'
            params = '-i 5 -p __dan -e rolåme -z'
            argv = [argv[0]] + params.split()
        opts = obj.parse_options(argv)
        result = obj.action(argv, opts)
        if type(result) == tuple and len(result) == 2:
            print('words_found: ', result[0])
            print(result[1])    
    
    main(sys.argv)
    
obj.main()
