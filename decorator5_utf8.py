# Example of using a decorator to predefine paramters


def utf8(func):
    def inner(*c):
        return func(*c, encoding='utf8')
    return inner


@utf8
def open(name, mode):
    pass


with open('temp.txt', 'r') as f:
    print(f.read())
    
