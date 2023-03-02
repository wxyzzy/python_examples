#! python3
#-*- coding: utf-8 -*-
#
# The above code says that Python 3.x should be used
# and that the text coding for this module is utf-8.
# PEP 3120 -- Using UTF-8 as the default source encoding
# This says that coding is utf-8 by default in Python 3.0 and later.
# So use the above coding line only if changing the source file
# to another coding standard.
#
# https://docs.python.org/3/using/windows.html
# https://docs.python.org/3/howto/unicode.html


import sys
import message1 as msg


def main(arg):
    msg.info('This is a main program.')
    msg.warning('Nothing to worry about.')
    return


if __name__ == "__main__":
    print(sys.argv[0])
    print(sys.argv[1:])
    print(sys.version)
    main(sys.argv)
    #a = input('hit return')
