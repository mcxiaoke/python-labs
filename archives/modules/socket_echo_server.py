#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-07-13 22:43:21

import socket

HOST = ''
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected from', addr
while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.sendall(data)
conn.close()
