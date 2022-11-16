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

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
print('[+] Server Started')

try:
    while True:
        print('[+] Listening For Client Message ...')
        message, client_addr = s.recvfrom(1024)
        message = message.decode()

        if message == 'REQUEST':
            print(f'[+] {client_addr} Client requested a command from the server')
            command_list = pull_list_from_str(input('Enter Command : '))

            if len(command_list) >= 1:
                s.sendto(command_list[0].encode(), client_addr)

                if command_list[0] == 'file' and len(command_list) >= 3:
                    s.sendto(command_list[2].encode(), client_addr)
                    s.sendto(read_file(command_list[1]).encode(), client_addr)
            else:
                print('Could not interpret command.')

            print('[+] Command sent')
            output = s.recv(1024)
            output = output.decode()
            print(f"Output: {output}")
        elif message == 'FILE':
            print('Request for file.')
        elif message == 'NAME':
            print('Request for filename.')

        else:
            print('received invalid request')

except ConnectionAbortedError:
    print('Client ended connection')
except KeyboardInterrupt:
    print('Terminated session.')
finally:
    s.close()

