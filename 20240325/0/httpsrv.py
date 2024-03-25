import sys
import socket

from http.server import test, SimpleHTTPRequestHandler

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()
print(HOST)
s.close()
PORT = '8000'
test(SimpleHTTPRequestHandler, port=int(PORT))
