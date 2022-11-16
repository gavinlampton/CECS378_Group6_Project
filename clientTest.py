import socket

defaultDestination = "127.0.0.1"
defaultDestinationPort = 4444
defaultPort = 42069

s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
try:
    buffer = b"test"

    print("sending data")
    s.sendto(buffer, (defaultDestination, defaultDestinationPort) )
    data = s.recv(4096)
    print(str(data))
finally:
    s.close()
