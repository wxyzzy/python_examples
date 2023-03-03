# Example of using a decorator design pattern

remote_functions = {}     # "send_to_server" decorated functions
function_fifo = []        # functions sent to server fifo

def check_server_for_function():
    # checks and executes saved functions
    global save_foo
    while function_fifo:
        item = function_fifo.pop(0)
        foo = remote_functions[item[0]]
        foo(*item[1:])
        
def send_to_server(func):
    if func.__name__ not in remote_functions:
        remote_functions.update({func.__name__: func})
    def inner(*p):
        global function_fifo
        function_fifo.append((func.__name__, *p))
        return func(*p)
    return inner


@send_to_server
def divide(a, b):
    print(a/b)


divide(2, 3)
divide(5, 2)
check_server_for_function()