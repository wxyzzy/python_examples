# The "with" statement catches errors and closes the file
# The "try" statement catches that error and lets you handle it.

try:
    with open('temp22.txt', 'r') as fin:
        s = fin.read()
        print(s)
except Exception as e:
    print(e)
    #raise(e)
print('Program continues...')
