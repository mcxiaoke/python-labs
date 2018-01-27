# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'
from xml.sax import ContentHandler
from  xml.sax import parse

import os


class XMLParserMixin():
    def __init__(self):
        pass

    def dispatch(self, prefix, name, attrs=None):
        mname = prefix + name.capitalize()
        dname = 'default' + prefix.capitalize()
        method = getattr(self, mname, None)
        if hasattr(method, '__call__'):
            args = ()
        else:
            method = getattr(self, dname, None)
            args = name,
        if prefix == 'start':
            args += attrs,
        if hasattr(method, '__call__'):
            method(*args)

    def startElement(self, name, attrs):
        self.dispatch('start', name, attrs)

    def endElement(self, name):
        self.dispatch('end', name)


class SiteBuilder(XMLParserMixin, ContentHandler):
    passthrough = False

    def __init__(self, directory):
        self.directory = [directory]
        self.ensure_directory()

    def ensure_directory(self):
        path = os.path.join(*self.directory)
        if not os.path.isdir(path):
            os.makedirs(path)

    def characters(self, content):
        if self.passthrough:
            self.out.write(content)

    def defaultStart(self, name, attrs):
        if self.passthrough:
            self.out.write('<' + name)
            for key, val in attrs.items():
                self.out.write(' %s="%s"' % (key, val))
            self.out.write('>')

    def defaultEnd(self, name):
        if self.passthrough:
            self.out.write('</%s>' % name)


    def startDirectory(self, attrs):
        self.directory.append(attrs['name'])
        self.ensure_directory()

    def endDirectory(self):
        self.directory.pop()

    def startPage(self, attrs):
        filename = os.path.join(*self.directory + [attrs['name'] + '.html'])
        self.out = open(filename, 'w')
        self.writeHeader(attrs['title'])
        self.passthrough = True

    def endPage(self):
        self.passthrough = False
        self.writeFooter()
        self.out.close()

    def writeHeader(self, title):
        self.out.write('<html>\n<head>\n <title>')
        self.out.write(title)
        self.out.write('</title>\n</head>\n <body>')

    def writeFooter(self):
        self.out.write('\n </body>\n</html>\n')


parse('site.xml', SiteBuilder('public_html'))

