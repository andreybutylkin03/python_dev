import socket
import shlex
import sys

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while data := conn.recv(1024):
            print(data, type(data))
            a = shlex.split(data.decode(), False, False)

            if len(a) > 1 and a[0] == 'print':
                conn.sendall(shlex.join(a[1:]).encode())
            if len(a) > 1 and a[0] == 'info':
                address, port = conn.get_extra_info('peername')
                if a[1] == 'port':
                    conn.sendall(port.encode())
                else:
                    conn.sendall(address.encode())
