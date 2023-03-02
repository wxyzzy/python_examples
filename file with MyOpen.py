# Supporting the "with" statement


class MyOpen:
    def __init__(self, filename, mode='r', encoding=None):
        self.f = open(filename, mode=mode, encoding=encoding)
        print('__init__ - file is opened)')

    def __enter__(self):
        print('__enter__ return file pointer')
        return self.f       # returned with "as" keyword

    def __exit__(self, errtype, errvalue, traceback):
        self.f.close()
        print('__exit__ - file is closed')
        print('error type - ' + str(errtype))


with MyOpen('temp.txt', 'r', encoding='utf-8') as fin:
    s = fin.read()
    print(s)
print('done')
