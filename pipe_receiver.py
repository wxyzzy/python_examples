import sys, os


#pause = input('>')

r = int(sys.argv[1])
print('read:', r, file=sys.stderr)

with os.fdopen(r, 'r') as fr:
    s = fr.readline().rstrip('\n')

print('received:', s, file=sys.stderr)
