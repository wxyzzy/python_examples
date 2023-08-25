# convert to class
# This converts globals to instance variables and functions to methods

# TO DO:
    # def methods to be saved in array and referenced as "self.method()"




def convert(source):
    token_chars = 'qwertyuiopåasdfghjklöäzxcvbnm_'
    end = '\n'
    s = ''
    s1 = ''
    first = True
    in_init = False
    var = []
    defs = []
    lines = source.split('\n')
    
    def leading(x):
        if type(x) == str:
            s = x.lstrip()
            return len(x) - len(s)
        elif type(x) == int:
            return ''.join([' ' for i in range(x)])
    
    def prepend_self(line):
        for v in (var + defs):
            if v == 'row_index' and v in line and 'label_char' in line:
                print(v)
            search_start = 0
            while v in line[search_start:] and search_start < len(line):
                istart = line[search_start:].index(v) + search_start
                iend = istart + len(v)
                remainder = line[iend:]
                non_token_char = remainder == '' or remainder[0] not in token_chars
                if istart >= 0 and non_token_char:
                    line = line[:istart] + 'self.' + line[istart:]
                search_start = iend + len('self.')
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
        for line in lines:
            start = leading(line)
            if start == len(line):
                s += end
            elif starts_with(line,'#', 'import', 'from'):
                if start == 0:
                    s += line + end
                else:
                    s += leading(start+4) + line + end
            else:
                if first:
                    s1 += 'class Klass:' + end
                    s1 += '    def __init__(self):' + end
                    first = False
                    in_init = True
                if line[start:start+6] == 'global':
                    pass
                elif line[start:start+3] == 'def':
                    if in_init:
                        s += s1 + end
                        in_init = False
                    x = line[start:].split('(')
                    if pass_ == 0:
                        defs.append(x[0][4:])
                    s2 = '(self' if x[1][0] == ')' else '(self, '
                    s += leading(4) + x[0] + s2 + x[1] + end
                elif start > 0:
                    s += leading(start+4) + prepend_self(line.lstrip()) + end
                elif start == 0 and ' = ' in line:
                    if pass_ == 0:
                        var.append(line.split(' = ')[0])
                    s1 += leading(8) + 'self.' + line + end
        s += 'k = Klass()' + end
        s += 'k.main()' + end
    return s

def main():
    print('start')
    with open('saob/word_helper.py', 'r', encoding='utf-8') as fin:
        source = fin.read()
        result = convert(source)
        with open('saob/word_helper_class.py', 'w', encoding='utf-8') as fout:
            fout.write(result)
    print('done')

main()
