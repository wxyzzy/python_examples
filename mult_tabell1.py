# make a multiplication table (non-pythonic)


s = ''
i = 0
while i < 9:
    i += 1
    s += '\t' + str(i)
s += '\n'
i = 0
while i < 9:
    i += 1
    s += str(i)
    j = 0
    while j < 9:
        j += 1
        s += '\t' + str(i*j)
    s += '\n'
print(s)


s = ''
for i in range(1, 10):
    s += '\t' + str(i)
s += '\n'
for i in range(1, 10):
    s += str(i)
    for j in range(1, 10):
        s += '\t' + str(i*j)
    s += '\n'
print(s)
