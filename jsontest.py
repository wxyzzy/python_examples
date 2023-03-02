# This shows reading JSON from string and file
# Then writing to JSON string and file
# ref: https://www.programiz.com/python-programming/json
# see also, https://docs.python.org/3/library/pickle.html


import json


x = '{"name":"Lisa", "age":[27, 35], "city":"Stockholm"}'
print(x)

# convert JSON string to Python object ("parsing")
person_dict = json.loads(x)
print(type(person_dict))
print(person_dict)
print()

# convert Python object to JSON
person_json = json.dumps(person_dict)
print(person_json)
print()

# write our JSON string to a text file of type ".json"
with open('person.json', 'w') as f:
    f.write(x)

# read JSON file and parse (making a Python object)
with open('person.json', 'r') as f:
    data = json.load(f)
print(type(data))
print(data)
