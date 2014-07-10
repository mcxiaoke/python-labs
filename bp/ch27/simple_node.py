# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

from xmlrpclib import ServerProxy
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys

from os.path import join, isfile


MAX_LENGTH = 6
OK = 1
FAIL = 2
EMPTY = ''


def get_port(url):
    'extract port from url'
    name = urlparse(url)[1]
    parts = name.split(':')
    return int(parts[1])


class Node:
    """
    p2p network node
    """

    def __init__(self, url, dirname, secret):
        self.url = url
        self.dirname = dirname
        self.secret = secret
        self.known = set()

    def query(self, query, history=[]):
        'query file, return file'
        code, data = self._handle(query)
        if code == OK:
            return code, data
        else:
            history += [self.url]
            if len(history) >= MAX_LENGTH:
                return FAIL, EMPTY
            return self._broadcast(query, history)

    def hello(self, other):
        'intro self to others'
        self.known.add(other)
        return OK

    def fetch(self, query, secret):
        if secret != self.secret:
            return FAIL
        code, data = self.query(query)
        if code == OK:
            f = open(join(self.dirname, query), 'w')
            f.write(data)
            f.close()
            return OK
        else:
            return FAIL

    def _start(self):
        'start rpc server'
        s = SimpleXMLRPCServer(('', get_port(self.url)), logRequests=False)
        s.allow_reuse_address = 1
        s.register_instance(self)
        s.serve_forever()

    def _handle(self, query):
        'handle request'
        dir = self.dirname
        name = join(dir, query)
        if not isfile(name):
            return FAIL, EMPTY
        return OK, open(name).read()

    def _broadcast(self, query, history):
        'broadcast query to all nodes'
        for other in self.known.copy():
            if other in history:
                continue
            try:
                s = ServerProxy(other)
                code, data = s.query(query, history)
                if code == OK:
                    return code, data
            except:
                self.known.remove(other)

        return FAIL, EMPTY


def main():
    url, directory, secret = sys.argv[1:]
    n = Node(url, directory, secret)
    n._start()


if __name__ == '__main__':
    main()

















