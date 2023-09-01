# convert to class
# This converts globals to instance variables and functions to methods

# TO DO:
    # def methods to be saved in array and referenced as "self.method()"




def convert(source):
    token_chars = 'qwertyuiopåasdfghjklöäzxcvbnm_'
    also = token_chars.upper()
    token_chars += also
    end = '\n'
    s = ''
    s1 = ''
    first = True
    in_init = False
    in_comment = False
    object_prefix = 'self.'
    var = []
    defs = []
    lines = source.split('\n')
    
    def leading(x):
        if type(x) == str:
            s = x.lstrip()
            return len(x) - len(s)
        elif type(x) == int:
            return ''.join([' ' for i in range(x)])
    
    def tokenize(line):
        # token is binary: "alphabetic" and "other"
        tokens = []
        sym = ''
        in_sym = True
        for ch in line:
            if in_sym:
                if ch in token_chars:
                    sym += ch
                else:
                    in_sym = False
                    tokens.append(sym)
                    sym = ch
            else:
                if ch not in token_chars:
                    sym += ch
                else:
                    in_sym = True
                    tokens.append(sym)
                    sym = ch
        if sym:
            tokens.append(sym)
            sym = ''
        return tokens
            
    def prepend_self(line):
        for v in (var + defs):
            tokens = tokenize(line)
            if True and v == 'parse_options' and v in line and 'parse_options' in line:
                print(v)
            s = ''
            for t in tokens:
                if t == v:
                    s += object_prefix
                s += t
            line = s       
        return line
    
    def starts_with(line, *substr):
        start = leading(line)
        for sub in substr:
            if line[start: start+len(sub)] == sub:
                return True
        return False
    
    for pass_ in range(2):
        s = ''
        s1 = ''
        first = True
        in_init = False
        in_comment = False
        test_area = False
        object_prefix = 'self.'
        for line in lines:
            start = leading(line)
            if 'if __name__' in line:
                test_area = True
                s += line + end
                s += leading(4) + 'obj = Klass()' + end
                object_prefix = 'obj.'
            elif test_area:
                s += leading(start) + prepend_self(line.lstrip()) + end
            elif start == len(line):
                s += end
            elif starts_with(line,'#', 'import', 'from'):
                if start == 0:
                    s += line + end
                else:
                    s += leading(4) + line + end
            elif in_comment and "'''" in line:
                s += line + end
                in_comment = False
            elif "'''" in line:
                in_comment = True
                s += line + end
            elif in_comment:
                s += line + end
            else:
                if first:
                    s1 += 'class Klass:' + end
                    s1 += '    def __init__(self):' + end
                    first = False
                    in_init = True
                if line[start:start+6] == 'global':
                    pass
                elif line[start:start+3] == 'def' and start == 0:
                    if in_init:
                        s += s1 + end
                        in_init = False
                    x = line[start:].split('(')
                    if pass_ == 0:
                        defs.append(x[0][4:])
                    s2 = '(self' if x[1][0] == ')' else '(self, '
                    s += leading(start + 4) + x[0] + s2 + x[1] + end
                elif start > 0:
                    s += leading(start+4) + prepend_self(line.lstrip()) + end
                elif start == 0 and ' = ' in line:
                    if pass_ == 0:
                        var.append(line.split(' = ')[0])
                    s1 += leading(8) + object_prefix + line + end
        if test_area:
            pass
        else:
            s += 'obj = Klass()' + end
            s += 'obj.main()' + end
    return s

def main():
    print('start')
    inname = "saob/word_helper.py"
    inname = "saob/word_helper_gui.py"
    outname = inname.split('.')
    outname = outname[0] + '_class.' + outname[1]
    with open(inname, 'r', encoding='utf-8') as fin:
        source = fin.read()
        result = convert(source)
        with open(outname, 'w', encoding='utf-8') as fout:
            fout.write(result)
    print('done')

main()
