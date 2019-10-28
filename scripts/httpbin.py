from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer


class GetHandler(SimpleHTTPRequestHandler):

    def handle_one_request(self):
        print("Client: {}".format(self.client_address[0]))
        return SimpleHTTPRequestHandler.handle_one_request(self)

    def do_GET(self):
        print(self.headers)
        SimpleHTTPRequestHandler.do_GET(self)


TCPServer(("", 8000), GetHandler).serve_forever()
