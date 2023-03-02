# The "with" statement catches errors and closes the file

with open('temp.txt', 'r') as fin:
    s = fin.read()
    print(s)
