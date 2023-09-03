import socket
SIZE = 4096

local_addr = ('localhost', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local_addr)

while True:
    data, a = sock.recvfrom(SIZE)
    print(a)
    print(data)