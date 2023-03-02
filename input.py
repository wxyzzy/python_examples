# Sample text input skript


def loop():
    done = False
    while not done:
        c = input("cmd> ")
        print("execute command " + c)

        # parsing of c goes here
        
        if c == 'quit':
            done = True


loop()
