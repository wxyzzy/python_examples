
import sys, os


msg = 'text written by child'

w = int(sys.argv[1])
print('write:', w, file=sys.stderr)

with os.fdopen(w, 'w') as fw:
    print(msg, file=fw)
    fw.flush()

print('written:', msg, file=sys.stderr)
