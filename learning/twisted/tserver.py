# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol


class SimpleLogger(Protocol):
    def connectionMade(self):
        print 'got connection from', self.transport.client

    def connectionLost(self, reason):
        print self.transport.client, 'disconnected.'

    def dataReceived(self, data):
        print 'data received:', data
        self.transport.write('data received.')


ft = Factory()
ft.protocol = SimpleLogger
reactor.listenTCP(1234, ft)
reactor.run()