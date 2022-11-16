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
            print(location)
            return_list[location] += c

    return return_list


HOST = 'localhost'
PORT = 4444

server = socket.socket()
server.bind((HOST, PORT))
print('[+] Server Started')
print('[+] Listening For Client Connection ...')

try:
    while True:
        server.listen(1)
        client, client_addr = server.accept()
        print(f'[+] {client_addr} Client connected to the server')

        try:
            while True:
                command_list = pull_list_from_str(input('Enter Command : '))

                if len(command_list) >= 1:
                    client.send(command_list[0].encode())

                    if command_list[0] == 'file' and len(command_list) > 1:
                        client.send(read_file(command_list[1]))

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

