# Sample text input skript
# type casting, switch, calling a function, string split


def mult(x):
    a, b = x
    print(float(a) * float(b))


def add(x):
    a, b = x
    print(float(a) + float(b))


def div(x):
    a, b = x
    print(float(a) / float(b))


def loop():
    switch = {'mult': mult, 'add': add, 'div': div}
    done = False
    while not done:
        response = input("cmd> ")
        lst = response.split(" ")
        try:
            cmd, param = lst[0], lst[1:]
            if cmd in switch:
                foo = switch[cmd]
                foo(param)
            elif cmd == 'quit':
                done = True
            else:
                print("unknown command")
        except Exception as e:
            print(e)

loop()
