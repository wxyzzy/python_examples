#!/usr/bin/env python
# -*- coding: utf-8 -*-

# references:
    # https://www.reportlab.com/docs/reportlab-userguide.pdf
    # https://www.programcreek.com/python/example/66708/reportlab.pdfgen.canvas.Canvas - example #11
# installation steps:
    # python -m pip freeze
    # python -m pip install reportlab
    

#import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import pink, black, red, blue, green


def test_A4_1cm():
    # https://www.programcreek.com/python/example/66708/reportlab.pdfgen.canvas.Canvas, example 12
    c = Canvas('pdf_drawing.pdf', pagesize=A4)
    c.translate(mm, mm)
    c.setStrokeColor(pink)
    #c.setFillColor(red)
    c.rect(10*mm,10*mm, 190*mm, 277*mm, fill=0)
    c.setStrokeColor(green)
    #c.setFillColor(green)
    c.circle(105*mm, 148*mm, 95*mm, fill=0)
    c.setStrokeColor("#555555")
    c.setLineWidth(0.2)
    y1 = 287
    for y0 in range(140, y1, 5):
        x1 = 10 + (y0 - 140) * 190 / 148
        x0 = 10
        c.line(x0*mm, y0*mm, x1*mm, y1*mm)
    c.line(10*mm, 140*mm, 200*mm, 156*mm)
    c.showPage()
    c.save() 
    
    
def main():
    try:
        test_A4_1cm()
    except Exception as e:
        print('File may be open - ' + str(e))
        raise(e)
    print('done')


main()
