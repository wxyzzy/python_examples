# multiplication table.  Very Pythonic.
# author: Erik Nash
# see also lambda2.py


for list_ in [[a*b for b in range(1, 10)] for a in range(1, 10)]:
    print(list_)
