import socket
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print("waiting on port:", port)


data, addr = s.recvfrom(1024)
print(data)

s.close()