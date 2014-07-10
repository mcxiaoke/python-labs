# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics import renderPDF

d = Drawing(200, 200)
s = String(100, 100, 'Hello, World!', textAnchor='middle')

d.add(s)
renderPDF.drawToFile(d, 'hello.pdf', 'A Simple PDF file')
