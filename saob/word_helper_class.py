# -*- coding: utf-8 -*-
# scripts for ORDEL game

import sys, os, re


            # this implies length, as in wordfeud
            # as in wordfeud
            # for example, if all letters may be used except these


        i - limit dictionary to n letter self.words
        a - enter accept letters that are allowed (self.wordfeud)
        r - enter required letters (wordel), can be a pattern like __r__
        e - enter exclude letters (wordel)
        p - enter accept pattern (including _ for wildcard)
        w - force self.wordfeud rules on pattern matching (not wordel)
        z - do analysis producing a list of self.words

       This removes self.words with r if in position 0, 2 and a if in position 4

class Klass:
    def __init__(self):
        self.accept_pattern = ''   # gives accept letters and positions (ignore '_')
        self.accept_letters = ''   # gives letters that may be used
        self.exclude_letters = ''  # exclude letters
        self.required_letters = '' # these letters are required
        self.wordfeud = False      # scan accept_pattern using wordfeud rule
        self.words = None
        self.help = '''
        self.where [options] = [option extra_word]

    def do_help(self, argv, i): print

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
            self.words = [w for w in whole if pat.match(w)]
        return self.words

    def get_random_word(self, word_length):
            import random
        self.words = self.get_word_list(word_length)
        n = len(self.words)
        i = random.randint(0, n)
        return self.words[i]

    def do_get_words(self, argv, i):
            # given word length, load words
        n = self.get_field(argv, i)
        self.words = self.get_word_list(n)

    def do_analysis(self, argv, i):
            # type of analysis depends on global variables 
        ap, al, el = self.accept_pattern, self.accept_letters, self.exclude_letters
        rl = self.required_letters.split(',')
        n = len(ap)
        allowed = [chr(x) for x in range(ord('a'), ord('z') + 1)]
        allowed += [x for x in 'åäö']
        allowed = al if al else allowed
        allowed = [x for x in allowed if x not in (el if el else '')]
        if ap == al == el == '':
                    # summarize number of words of various lengths
            print('word_len\tn_found\texample')
            for n in range(1, 40):
                self.words = self.get_word_list(n) 
                n_found = len(self.words)
                print(str(n) + '\t' + str(n_found) + '\t' + ', '.join(self.words[:5]))
        elif n:
    def test(self, w):
                nonlocal allowed
                if ap and self.wordfeud:
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
                        if ch in self.exclude_letters:
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
            do_get_self.words(argv, i)
                    #print('original words: ', len(words))
            self.words = [w for w in self.words if self.test(w)]
            self.words = list(set(self.words))
            self.words.sort()
            n_found = len(self.words)
            return n_found, self.words


    def do_accept_pattern(self, argv, i):
        x = self.get_field(argv, i)
        self.accept_pattern = x

    def do_accept_letters(self, argv, i):
        x = self.get_field(argv, i)
        self.accept_letters = x

    def do_exclude_letters(self, argv, i):
        x = self.get_field(argv, i)
        self.exclude_letters = x

    def do_required_letters(self, argv, i):
        x = self.get_field(argv, i)
        self.required_letters = x

    def do_wordfeud(self, argv, i):
        self.wordfeud = True

    def action(self, argv, opts):
            # do something for various '-' options
        switch = {'h':do_self.help, 'i':do_get_self.words, 'p':do_self.accept_pattern,
                  'a':do_self.accept_letters, 'e':do_self.exclude_letters, 
                  'r':do_self.required_letters, 'w':do_self.wordfeud, 'z':self.do_analysis}
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
        opts = self.parse_options(argv)
        result = self.action(argv, opts)
        return result

    def main(self, argv):
            # parse for '-' options
        n = len(argv)
        if n <= 1:
                    # example from wordfeud where given pattern and allowed char is used
            params = '-w -p lla -a slixel -z'
                    # example from wordel where word length is 5'
            params = '-i 5 -p __dan -e rolåme -z'
            argv = [argv[0]] + params.split()
        opts = self.parse_options(argv)
        result = self.action(argv, opts)
        if type(result) == tuple and len(result) == 2:
            print('words_found: ', result[0])
            print(result[1])    

        self.main(sys.argv)

k = Klass()
k.main()
