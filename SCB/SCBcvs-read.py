# This is an example of reading a CSV downloaded from SCB.se


import csv
from pprint import pprint


def read_csv():
    with open('SCB202011.csv', 'r') as fcsv:
        csv_data = csv.reader(fcsv, delimiter=',')
        pprint(csv_data)
        rows = [x for x in csv_data]
        #pprint(rows)
        return rows
    
def unpack_rows(rows):
    # This is specific to rows (message, empty, title, data)
    message = rows[0][0]
    title_row = rows[2]
    data = rows[3:]
    return message, title_row, data

def interpret_data(titles, data):
    # This is specific to the data structure
    # Assumes that data is in tuples of string (name, number)
    titles = tuple(titles)
    data2 = [(name, int(num)) for name, num in data]
    #pprint(data2)
    return titles, data2
    
rows = read_csv()
pprint(rows)
print()
message, titles, data = unpack_rows(rows)
titles, data2 = interpret_data(titles, data)
pprint(message)
pprint(titles)
pprint(data2)
