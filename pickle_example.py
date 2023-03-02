# This shows reading Pickle from string and file
# Then writing to Pickle string and file
# Pickle


import pickle

# define a Python object
x = {"name": "Lisa", "age": [27, 35], "city": "Stockholm"}

print('Original Python dictionary:')
print(str(x))
print()

print('Conversion to pickle shown as a byte string:')
person_pickle = pickle.dumps(x)
print(person_pickle)
print()

print('Convert pickle byte string to Python object ("interpreting"):')
y = pickle.loads(person_pickle)
print(str(y))
print()

# save Python object in a file
x1 = {"name": "Måns", "age": (28, 38), "city": "Kalmar"}
with open('pickle.pckl', 'wb') as fout:
    pickle.dump(x1, fout)
    print('write to file:  ' + str(x1))

# read Pyton object from a file
with open('pickle.pckl', 'rb') as fin:
    y1 = pickle.load(fin)
    print('read from file: ' + str(y1))
