# sqlite test - too simple for safe use


import sqlite3
from datetime import datetime
from datetime import date


dbname = 'example32.db'

allfields = ['created', 'description', 'quantity', 'amount']
sfields = ', '.join(allfields)
sfields2 = 'id integer not null primary key, ' + sfields
values = ['"'+str(datetime(2020, 2, 15))+'"', '"IBM"', str(2), str(300.8)]
svalues = ', '.join(values)
print(svalues)

conn = sqlite3.connect(dbname)
conn.execute('CREATE TABLE stocks ({})'.format(sfields))
conn.execute('INSERT INTO stocks ({}) VALUES ({})'.format(sfields, svalues))
res = conn.execute('SELECT {} FROM stocks'.format(sfields))
print(res)
conn.commit()
conn.close()
