'''
File: udp_receiver.py
Created: 2021-04-02 14:30:43
Modified: 2021-04-02 14:30:47
Author: mcxiaoke (github@mcxiaoke.com)
License: Apache License 2.0
'''

import socket
import struct
import sys
import click
from datetime import datetime
from socketserver import BaseRequestHandler, ThreadingUDPServer, ThreadingMixIn, UDPServer

from click.decorators import pass_obj


class MessageHandler(BaseRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle(self):
        data, sock = self.request
        if(len(data) < 3):
            print(data)
        try:
            self.extras = self.server.extras
            keyword, ip = self.extras
            text = data.decode('utf8').replace('\r\n', '').replace('\n', '')
            should_print = (not keyword or (keyword in text)) and (
                not ip or (ip in self.client_address[0]))
            if should_print:
                addr = self.client_address[0]
                date_prefix = datetime.strftime(datetime.now(), '%H:%M:%S')
                print('[{}][{}]: {}'.format(date_prefix, addr, text))
        except Exception as e:
            print('Can not parse:', data)


class ThreadedUDPMonitor(ThreadingMixIn, UDPServer):

    def __init__(self, server_address, RequestHandlerClass, extras):
        super().__init__(server_address, RequestHandlerClass)
        self.extras = extras


@click.command()
@click.option('-k', '--keyword',
              help='Message text content match keyword')
@click.option('-i', '--ip', help='Message source ip filter')
@click.argument('port', required=True, default=10000, type=click.IntRange(2000, 60000))
def monitor(port, keyword, ip):
    '''Simple UDP Message Monitor'''
    print('UDP Data Monitor on port {} (keyword:{}, ip:{})'.format(port, keyword, ip))
    print('====================================')
    serv = ThreadedUDPMonitor(('', port), MessageHandler, (keyword, ip))
    serv.serve_forever()


if __name__ == '__main__':
    monitor()


'''
multicast_group = '224.0.0.255'
server_address = ('0.0.0.0', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)

print('UDP Serial Monitor Started.')

# Receive/respond loop
while True:
    # print('\nwaiting to receive message')
    data, address = sock.recvfrom(256)
    date_prefix = datetime.strftime(datetime.now(), '%H:%M:%S')
    print('[{}][{}]: {} ({})'.format(date_prefix, address[0], data.decode(
        'utf8')[1:].replace('\n', ''), len(data)))
'''
