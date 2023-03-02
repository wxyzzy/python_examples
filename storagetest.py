# Testing storage.py and transaction.py


from storage import Memory
from transaction import Transaction
from pprint import pprint
from datetime import datetime
from datetime import date


with Memory('example18.db') as m:
    with Transaction(m.conn, "IMMEDIATE") as cursor:
        if False:
            m.create_table('stocks',
                [('created', datetime), ('description', str),
                ('quantity', float), ('amount', float)])
            m.insert('stocks', ['created', 'description', 'quantity', 'amount'], [
                datetime(2020, 2, 15), 'IBM', 2, 300.2])
            m.insert('stocks', ['description', 'quantity',
                'amount'], ['Apple', 22, 34.2])
        result = m.select('stocks', ['description', 'quantity', 'amount'],
                'quantity > ?', ['20'])
        pprint(result)
        if len(result) > 0:
            n = result[0][1]
        
            m.update('stocks', ['created', 'quantity'], [
               date.today(), n + 1], 'description=?', ['Apple'])

            result = m.select('stocks', ['description', 'quantity', 'amount'],
                'quantity > ?', ['20'])
            pprint(result)
