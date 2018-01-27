# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import socket

port = 1234
host = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall('hello, server, are you crazy?\n')
data = s.recv(1024)
print data
s.close()