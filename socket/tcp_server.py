# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

from SocketServer import TCPServer, ForkingMixIn, StreamRequestHandler


class Server(TCPServer, ForkingMixIn): pass


class Handler(StreamRequestHandler):
    def handle(self):
        addr = self.request.getpeername()
        print 'connection from ', addr
        self.wfile.write('welcome to this server!')
        print self.rfile.read(1024)


server = Server(('', 1234), Handler)
server.serve_forever()