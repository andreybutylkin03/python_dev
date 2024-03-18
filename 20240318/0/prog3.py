import sys
import shlex
import socket

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    while msg := sys.stdin.buffer.readline():
        a = shlex.split(msg.rsplit().decode(), False, False)
        print(a)

        if len(a) > 1 and a[0] == 'print':
            s.sendall(shlex.join(a[1:]))
        if len(a) > 1 and a[0] == 'info':
            address, port = s.get_extra_info('peername')
            if a[1] == 'port':
                s.sendall(port)
            else:
                s.sendall(address)
