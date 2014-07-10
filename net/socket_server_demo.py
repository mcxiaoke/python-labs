# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

from SocketServer import TCPServer, StreamRequestHandler


class Handler(StreamRequestHandler):
    def handle(self):
        addr = self.request.getpeername()
        print 'got connection from', addr
        self.wfile.write('welcome for connecting')
        print self.rfile.read(1024)


ADDRESS = ('', 1234)
server = TCPServer(ADDRESS, Handler)
server.serve_forever()
