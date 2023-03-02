# This is an example of an exception (ZeroDivisionError)
# Undantag == Exception


import sys
import traceback


try:
    a = 0
    b = 5 / a
except Exception as e:
    print('TRACEBACK:')
    print(traceback.format_exc())

    print('SYS.EXCINFO')
    print(sys.exc_info()[0])

    print('EXCEPTION')
    print(type(e))
    print(e)
    raise(e)
else:
    print('ok')
finally:
    print('finally')
print('program continuous')
