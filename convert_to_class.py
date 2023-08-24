# convert to class
# This converts globals to instance variables and functions to methods


def leading(x):
    if type(x) == str:
        s = x.lstrip()
        return len(x) - len(s)
    elif type(x) == int:
        return '                                                        '[:x]

def convert(source):
    end = '\n'
    s = ''
    s1 = ''
    first = True
    in_init = False
    var = []
    lines = source.split('\n')
    
    def prepend_self(line):
        for v in var:
            last_index = 0
            while v in line[last_index:]:
                i = line[last_index:].index(v)
                if i >= 0:
                    j = last_index + i
                    line = line[:j] + 'self.' + line[j:]
                    last_index = j + 6
        return line
                
    for line in lines:
        start = leading(line)
        if start == len(line):
            s += end
        elif line[start] == '#':
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
                s2 = '(self' if x[1][0] == ')' else '(self, '
                s += leading(4) + x[0] + s2 + x[1] + end
            elif start > 0:
                s += leading(start+4) + prepend_self(line.lstrip()) + end
            elif start == 0 and ' = ' in line:
                var.append(line.split(' = ')[0])
                s1 += leading(8) + 'self.' + line + end
    s += 'k = Klass()' + end
    s += 'k.main()' + end
    return s

def main():
    print('start')
    with open('saob/word_helper_gui.py', 'r') as fin:
        source = fin.read()
        result = convert(source)
        with open('saob/word_helper_gui_class.py', 'w', encoding='utf-8') as fout:
            fout.write(result)
    print('done')

main()
