# This module manipulates an sqlite database
# ref: https://docs.python.org/3/library/sqlite3.html


from datetime import datetime
import sqlite3


dbname = 'example8.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()
conn.close()


def create_table(conn, name, fields):
    # fields is a list of (name, type) tuplet pairs
    # CREATE TABLE stocks (date text, description text, qty real, price real)
    def f(y):
        typemap = {datetime: 'date', float: 'real', str: 'text'}
        if y in typemap:
            z = typemap[y]
        else:
            raise ValueError('Unknown type for sqlite mapping.')
        return z
    pairs = [(x, f(y)) for x, y in fields]
    print(pairs)
    sfields = ', '.join([' '.join((x, y)) for x, y in pairs])
    s = 'CREATE TABLE {} ({})'.format(name, sfields)
    print(s)
    conn.execute(s)


conn = sqlite3.connect(dbname)
c = conn.cursor()
d = datetime(2020, 4, 15)
create_table(conn, 'stocks',
             [('created', datetime), ('description', str),
              ('quantity', float), ('amount', float)])
conn.close()
