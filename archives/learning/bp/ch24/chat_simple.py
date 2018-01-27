# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

from asyncore import dispatcher
import asyncore
import socket


class ChatServer(dispatcher):
    def __init__(self, host, port):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        conn, addr = self.accept()
        print 'connection from', addr[0]


if __name__ == '__main__':
    s = ChatServer('', 8001)
    asyncore.loop()