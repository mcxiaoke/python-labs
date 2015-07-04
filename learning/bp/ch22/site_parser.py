# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

from xml.sax import ContentHandler
from xml.sax import parse


class TestHandler(ContentHandler):
    def startElement(self, name, attrs):
        print name, attrs.keys()


class HeadlineHandler(ContentHandler):
    inside = False

    def __init__(self, headlines):
        ContentHandler.__init__(self)
        self.headlines = headlines
        self.data = []

    def startElement(self, name, attrs):
        if name == 'h1':
            self.inside = True

    def endElement(self, name):
        if name == 'h1':
            text = "".join(self.data)
            self.data = []
            self.headlines.append(text)
            self.inside = False

    def characters(self, content):
        if self.inside:
            self.data.append(content)


headlines = []
parse('site.xml', HeadlineHandler(headlines))
print 'found h1 elements:'
for h in headlines:
    print h


