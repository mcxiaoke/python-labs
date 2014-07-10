# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import socket

HOST = ''
PORT = 1238
ADDRESS = (HOST, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'socket created.'
s.bind(ADDRESS)
print 'socket bind.'
s.listen(1)
print 'socket listen'
while True:
    conn, address = s.accept()
    try:
        conn.settimeout(5)
        buffer = conn.recv(1024)
        if buffer == 'bye':
            print 'goodbye,quit!'
            conn.close()
            break
        elif buffer == '1':
            print 'welcome to server!'
            conn.send('welcome to server!')
        else:
            print buffer
            conn.send('pin is wrong, go out!')
    except socket.timeout:
        print 'time out'
    conn.close()
