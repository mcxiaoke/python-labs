#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-07-13 22:43:30

import socket

HOST = 'localhost'
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('hello, server!')
data = s.recv(1024)
s.close()
print 'Received', repr(data)
