# This module manipulates an sqlite database
# This might be called a "wrapper" to make calls more convenient
# ref: https://docs.python.org/3/library/sqlite3.html

from pprint import pprint
from datetime import datetime
from datetime import date
import sqlite3
datepat = '%Y-%m-%d %H:%M:%S'
debug = True


def map_to_datetime(x):
    # Map date from sql text to python datetime
    # A weak solution depending on dateformat
    y = x
    if type(x) == str and ''.join([a for a in x if a in '-:']) == '--::':
        y = datetime.strptime(x, datepat)
    return y


class Memory:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)

    def __enter__(self):
        return self

    def __exit__(self, errtype, errvalue, traceback):
        if not errtype:
            self.commit()
        self.close()

    def commit(self):
        if self.conn:
            self.conn.commit()
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        
    def create_table(self, name, fields):
        # fields is a list of (name, type) tuplet pairs
        # CREATE TABLE stocks (date text, description text, qty real, price real)
        conn = self.conn
        c = conn.cursor()
        try:
            primary = [('id', 'integer not null primary key')]
            def f(y):
                typemap = {datetime: 'text', float: 'real', int: 'integer', str: 'text'}
                if y in typemap:
                    z = typemap[y]
                else:
                    conn.close()
                    raise ValueError('Unknown type for sqlite mapping.')
                return z
            pairs = [(x, f(y)) for x, y in fields]
            sfields = 'id integer not null primary key, '
            sfields += ', '.join([' '.join((x, y)) for x, y in pairs])
            sql = 'CREATE TABLE {} ({})'.format(name, sfields)
            if debug:
                print(sql)
            conn.execute(sql)
        except:
            self.close()
            raise Exception('Create table failed: table might exist.')
            return

    def insert(self, table, fields, values):
        # table is the name of the table
        # fields is a list of names
        # values is a list of values to store in respective fields
        # INSERT INTO stocks (date, description, qty, price) VALUES(?,?,?,?)
        conn = self.conn
        c = conn.cursor()
        try:
            sfields = ', '.join(fields)
            values = [x.strftime(datepat) if type(x) in (
                datetime, date) else x for x in values]
            svalues = ', '.join(["?".format(x) for x in values])
            sql = 'INSERT INTO {} ({}) VALUES ({})'.format(
                table, sfields, svalues)
            if debug:
                print(sql)
            conn.execute(sql, values)
        except:
            self.close()
            raise Exception('Insert failed.')
            return

    def update(self, table, fields, values, where=None, wherevalues=[]):
        # table is the name of a table
        # fields is a list of field names
        # values is a list of values to store in respective fields
        # UPDATE table SET field1=value1, field2=value2, ... where_clause
        # where_clause contains question marks filled by wherevalues
        conn = self.conn
        c = conn.cursor()
        try:
            sfields = ', '.join(['{}=?'.format(x) for x in fields])
            sql = 'UPDATE {} SET {}'.format(table, sfields, )
            if where:
                sql += ' WHERE {}'.format(where)
                values += wherevalues
            if debug:
                print(sql)
            values = [x.strftime(datepat) if type(x) in (
                datetime, date) else x for x in values]
            conn.execute(sql, values)
        except Exception as e:
            self.close()
            raise Exception('Udate failed: {}'.format(e))
            return

    def select(self, table, fields, where=None, values=[]):
        # table is the name of a table
        # fields is a list of fields to be selected
        # where is a string which is a where clause containing question marks (?)
        # values is a list of values to fill in the question marks
        # SELECT field1, field2, ... FROM table WHERE where_clause
        # returns a list of tuples as specified by fields
        conn = self.conn
        c = conn.cursor()
        try:
            sfields = ', '.join(fields)
            sql = 'SELECT {} FROM {}'.format(sfields, table)
            if where:
                sql += ' WHERE {}'.format(where)
            if debug:
                print(sql)
            res = list(conn.execute(sql, values))
            result = [tuple(map_to_datetime(x) for x in tup) for tup in res]
        except Exception as e:
            self.close()
            raise Exception('Select failed: {}'.format(e))
            return
        return result

    def execute(self, sql, values=[]):
        # convenience wrapper that just passes sql to sqlite
        conn = self.conn
        c = conn.cursor()
        try:
            if debug:
                print(sql)
            res = list(conn.execute(sql, values))
            result = [tuple(map_to_datetime(x) for x in tup) for tup in res]
        except Exception as e:
            self.close()
            raise Exception('Select failed: {}'.format(e))
            return
        return result


if debug and __name__ == "__main__":
    with Memory('example9.db') as m:
        m.create_table('stocks',
                     [('created', datetime), ('description', str),
                     ('quantity', float), ('amount', float)])
        m.insert('stocks', ['created', 'description', 'quantity', 'amount'], [
                 datetime.today(), 'IBM', 2, 300.2])
        #m.insert('stocks', ['description', 'quantity',
        #                    'amount'], ['Apple', 22, 34.2])
        m.update('stocks', ['created', 'quantity'], [
             date.today(), 226], 'description=?', ['Apple'])
        #m.execute(
        #    'update stocks set quantity = 333 where description = ?', ['Apple'])
        #print(m.execute('select description from stocks where amount < ?', [50]))
        #pprint(
        #    m.select('stocks', ['created', 'description', 'quantity', 'amount']))
        #pprint(m.select('stocks', ['description', 'quantity', 'amount'],
        #                'quantity > ?', ['20']))
        #m.close()
