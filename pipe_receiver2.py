# pipe_receiver2.py
# ref in part Henrik Tunedal


import sys

print(*(f'Got line: {line.rstrip()}' for line in sys.stdin), sep='\n')
