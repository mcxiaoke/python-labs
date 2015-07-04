# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import asyncore
import asynchat

class RequestHandler(asynchat.async_chat):

    def __init__(self,sock,addr,sessions,log):
        asynchat.async_chat.__init__(self,sock=sock)
        self.addr=addr
        self.sessions=sessions
        self.ibuffer=[]
        self.obuffer=""
        self.set_terminator("\r\n\r\n")
        self.reading_headers=True
        self.handing=False
        self.cgi_data=None
        self.log=log

    def collect_incoming_data(self, data):
        """buffer the data"""
        self.ibuffer.append(data)

    def found_terminator(self):
        if self.reading_headers:
            self.reading_headers=False
            self.parse_headers("".join(self.ibuffer))
            self.ibuffer=[]
            if self.op.upper()=="POST":
                clen=self.headers.getheader("content-length")
                self.set_terminator(int(clen))
            else:
                self.handing=True
                self.set_terminator(None)
                self.handle_request()

        elif not self.handing:
            self.set_terminator(None)
            # self.cgi_data=parse(self.headers,"".join(self.ibuffer))
