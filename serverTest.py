import socket


port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print("waiting on port:", port)

try:
    data, addr = s.recv(1000)
    print("Received {0}" % data)
    data = str.capitalize(str(data))
    s.sendto(bytes(data), addr)

finally:
    s.close()
