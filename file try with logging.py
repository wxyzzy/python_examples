# The "with" statement catches errors and closes the file
# The "try" statement catches that error and lets you handle it.
# The "logging.error" statement writes the error to a file.


import logging


logging.basicConfig(filename='file_try.log',
                    level=logging.WARNING,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S')


try:
    with open('temp22.txt', 'r') as fin:
        s = fin.read()
        print(s)
except Exception as e:
    print(e)
    logging.error(e)
print('Program continues...')
