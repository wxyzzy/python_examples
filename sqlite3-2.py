# sqlite test - attempt to make simple



import sqlite3
from datetime import datetime
from datetime import date
from pprint import pprint


dbname = 'example46.db'
newdb = True

conn = sqlite3.connect(dbname)

table = 'stocks'
allfields = ['created', 'description', 'quantity', 'amount']

try:
    if newdb:
        sfields = ', '.join(allfields)
        sfields2 = 'id integer not null primary key, ' + sfields
        sql = 'CREATE TABLE {} ({})'.format(table, sfields2)
        print('create:')
        print(sql)
        conn.execute(sql)
        
        print()
        datepat = '%Y-%m-%d %H:%M:%S'
        fields = ', '.join(allfields[1:])
        values = [datetime(2020, 2, 15), 'IBM', 2, 300.2]
        values2 = [x.strftime(datepat) if type(x) in (
                    datetime, date) else x for x in values]
        svalues = ', '.join(["?".format(x) for x in values2])
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(
                    table, sfields, svalues)
        print('insert:')
        print(sql)
        print(values)
        conn.execute(sql, values)
        conn.commit()
except Exception as e:
    print(e)
        
print()
sfields = ', '.join(allfields)
sql = 'SELECT {} FROM {}'.format(sfields, table)
print('select:')
print(sql)
res = list(conn.execute(sql))
print(res)

conn.close()

