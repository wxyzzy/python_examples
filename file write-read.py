# Write and read to file
# Tip: right-click to set a break-point

def test_file():
    fout = open('temp.txt', 'w')
    s = 'This text, saved in file'
    fout.write(s)
    print('Text written to file: ' + s)
    fout.close()

    fin = open('temp.txt', 'r')
    s1 = fin.read()
    fin.close()
    print('Text read from file:  ' + s1)


test_file()
