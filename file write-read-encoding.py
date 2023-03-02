# Write to file with utf-8 and read binary
# Tip: right-click to set a break-point

def test_file():
    fout = open('temp.txt', 'w', encoding='utf8')
    s = 'Vi försöker skriva svenska bokstäver ---åäö---.'
    fout.write(s)
    print('Text written to file: ' + s)
    fout.close()

    # The following reads binary
    fin = open('temp.txt', 'rb')
    s1 = fin.read()
    fin.close()
    print('\nWe read a binary file:')
    print(s1)

    # The following ascii encoding fails to read
    fin = open('temp.txt', 'r', encoding='ascii')
    s1 = fin.read()
    fin.close()
    print('\nWe read an ascii file: ' + s1)


test_file()
