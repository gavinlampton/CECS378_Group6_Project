import socket


port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print("waiting on port:", port)

try:
    data, addr = s.recvfrom(4096)
    print("Received {0}" % data)
    data = str.capitalize(str(data))
    s.sendto(bytes(data, 'utf-8'), addr)

finally:
    s.close()
