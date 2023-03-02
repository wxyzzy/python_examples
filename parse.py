# Example of parsing input arguments
#-*- coding: utf-8 -*-


import sys, json, pickle

help = '''
parse [[options] file]
options:
    -i initialize data
    -J jason write
    -j jason read
    -P pickle write
    -p pickle read
    -o output to console
This script alternates between read and write. It always
replaces file extensions, for example with "json" or "pckl".
If called without arguments, it defaults to "-iJjPpo".
    '''
def do_help(argv, i): print(help)


obj = {"name":"Åsa", "age":[29, 35], "city":"Malmö"}
data = None    #object of interest


def get_filename(argv, i, ext):
    # file name may appear in the i+1 position
    if i+1 >= len(argv): return 'parse.' + ext
    elif argv[i+1][0] == '-': return 'parse.' + ext
    else:
        lst = argv[i+1].split('.')
        return lst[0] + '.' + ext

def do_init(argv, i):
    global data
    data = obj

def do_json_read(argv, i):
    global data
    filename = get_filename(argv, i, 'json')
    with open(filename, 'r') as f:
        data = json.load(f)

def do_json_write(argv, i):
    global data
    filename = get_filename(argv, i, 'json')
    with open(filename, 'w') as f:
        json.dump(data, f)

def do_pickle_read(argv, i):
    global data
    filename = get_filename(argv, i, 'pckl')
    with open(filename, 'rb') as f:
        data = pickle.load(f)

def do_pickle_write(argv, i):
    global data
    filename = get_filename(argv, i, 'pckl')
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def do_output(argv, i):
    global data
    print(data)

def action(argv, opts):
    # do something for various '-' options
    switch = {'h':do_help, 'i':do_init, 'j':do_json_read, 'J':do_json_write,
              'p':do_pickle_read, 'P':do_pickle_write, 'o':do_output}
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
        argv = [argv[0]] + ['-iJjPpo'] + ['parse.txt']
    opts = parse_options(argv)
    action(argv, opts)

if __name__ == "__main__":
    main(sys.argv)

