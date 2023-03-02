# This writes a multiplication table in sheet 'mult'
# Parts taken from Henrik Tunedal


import openpyxl
import os
from os import path

filename = 'excel_test.xlsx'


def dump_to_excel(filename, sheets):
    import time; t = time.time()
    wb = openpyxl.Workbook()
    for name, rows in sheets.items():
        ws = wb.create_sheet(title=name)
        for i, row in enumerate(rows):
            ws.append(row)
    print("Write file:", filename)
    wb.save(filename)
    print("Dumped {} rows in {:.2f} seconds.".format(i+1, time.time() - t))

def make_test_data():
    sheets = {}
    name = 'mult'
    lst = [[x*y for x in range(1, 10)] for y in range(1, 10)]
    sheets.update({name: lst})
    return sheets

def test_dump_to_excel():
    if path.exists(filename):
        os.remove(filename)
    sheets = make_test_data()
    dump_to_excel(filename, sheets)

test_dump_to_excel()
