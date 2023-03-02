#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This sample is very crude, but works.  Keep for reference.
# https://www.blog.pythonlibrary.org/2012/07/18/parsing-xml-and-creating-a-pdf-invoice-with-python/
# installation steps:
    # python -m pip freeze
    # python -m pip install reportlab
    

import reportlab

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table, TableStyle
from reportlab.graphics import shapes

# The following myFirstPage, myLaterPages, go() come from, https://www.reportlab.com/docs/reportlab-userguide.pdf, page 65.
# build a simple multi-page pdf
from reportlab.rl_config import defaultPageSize
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
pageinfo = "deltagare journalutdrag"

def myFirstPage(canvas, doc):
    canvas.saveState()
    #canvas.setFont('Times-Bold',16)
    #canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, "Hello world")
    canvas.setFont('Times-Roman',9)
    canvas.drawString(mm, 0.20 * mm, "Sida {} {}".format(doc.page, pageinfo))
    canvas.restoreState()

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(mm, 0.20 * mm, "Sida {} {}".format(doc.page, pageinfo))
    canvas.restoreState()
    
def startsWith(line, key):
    # starts with key and next char is not key[0]
    return len(line) > len(key) + 1 and line[:len(key)] == key and line[len(key)] != key[0]
    
def md2html(line):
    bb = line.replace('***', '<i><b>').replace('**', '<b>').replace('*', '<i>')
    for sym, sim2 in [('<i>','</i>'),('<b>','</b>')]:
        aa = bb.split(sym)
        bb = ''
        for i,a in enumerate(aa):
            bb = bb + a + ('' if i == len(aa) - 1 else sym if i % 2 == 0 else sim2)
    bb = bb.replace('</i></b>','</b></i>')    # close of bold and italics must mirror open
    return bb

def drawsomething():
    # draw something to PDF where "s" is a reportlab "flowable"
    d = shapes.Drawing(300, 50)
    for i in range (10):
        d.add(shapes.Line(0, 5 * i, 300 - 30 * i, 0))
    return d
    
def parse(str0, outname):
    doc = SimpleDocTemplate(outname)
    Story = [Spacer(1, 5*mm)]
    normal = styles["Normal"]
    heading1 = styles["Heading1"]
    heading1.spaceBefore = 12
    heading2 = styles["Heading2"]
    heading3 = styles["Heading3"]
    heading4 = styles["Heading4"]
    #print(heading1.listAttrs())     # see what attributes are set
    lines = str0.splitlines()
    for line in lines:
        if len(line) == 0:
            p = Paragraph('', normal)
        elif startsWith(line, '#'):
            p = Paragraph(line[1:], heading1)
        elif startsWith(line, '##'):
            p = Paragraph(line[2:], heading2)
            Story.append(p)
            p = drawsomething()
        elif startsWith(line, '###'):
            p = Paragraph(line[3:], heading3)
        elif startsWith(line, '####'):
            p = Paragraph(line[4:], heading4)
        else:
            p = Paragraph(md2html(line), normal)
        Story.append(p)
        #Story.append(Spacer(1, 5*mm))
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

def flowablestest():
    inname = 'pdf_flow.txt'
    outname = 'pdf_flow.pdf'
    with open(inname, 'r') as f:
        teststr = f.read()
    print('Look at: ' + outname)
    parse(teststr, outname)

def main():
    flowablestest()
    print('done')

main()
