import socket
import string


def read_file(file):
    return_value = ''

    try:
        f = open(file)
        return_value = f.read()

    except FileNotFoundError as e:
        print(e)

    return return_value


def pull_list_from_str(input_string):
    return_list = ['']
    location = 0
    for c in input_string:
        if c in string.whitespace:
            location += 1
            return_list.append('')
        else:
            return_list[location] += c

    return return_list


HOST = 'localhost'
PORT = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
print('[+] Server Started')
print('[+] Listening For Client Connection ...')

try:
    while True:
        data, client_addr = server.recvfrom(1024)
        print(f'[+] {client_addr} Client requested a command from the server')

        try:
            while True:
                command_list = pull_list_from_str(input('Enter Command : '))

                if len(command_list) >= 1:
                    server.sendto(command_list[0].encode(), client_addr)

                    if command_list[0] == 'file' and len(command_list) >= 3:
                        server.sendto(command_list[2].encode(), client_addr)
                        server.send(read_file(command_list[1]).encode(), client_addr)

                else:
                    print('Could not interpret command.')

                print('[+] Command sent')
                output = client.recv(1024)
                output = output.decode()
                print(f"Output: {output}")
        except ConnectionAbortedError:
            print('Client ended connection')
except KeyboardInterrupt:
    print('Terminated session.')
finally:
    server.close()

