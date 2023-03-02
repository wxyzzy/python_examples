# Script which imports our own module
# and calls a function.


import message1
from message1 import info

print('begin test')

message1.foo('"Message 1", is a simple text.')
message1.warning('Another message to print.')
info('Information')

print('done test')
