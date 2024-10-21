# echo_server.py
#
# Create a server and client running in separate threads, using
# sockets to send data back and forth

import socket
import threading
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Function to create the server:
def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Server attempting to bind port')
    server.bind((HOST, PORT))
    print('Server waiting for client connection')
    server.listen(3)
    conn, addr = server.accept()   # blocking call
    print(f'Server connected by {addr}')
    while True:
        print(f'Connection request from {addr}')
        data = conn.recv(1024)
        data_upper = str(data).upper()
        data = bytes(f'Server received: {data_upper}', 'utf-8')
        conn.sendall(data)

# Start the server in a new thread:
print('Starting server\n')
t = threading.Thread(target=server)
t.start()

time.sleep(0.5)  # wait a moment to make sure the server is ready

# Start the client and talk to the server:
print('Client attempting to create socket')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Client attempting to connect to port')
client.connect((HOST, PORT))
send_data = b'Hello server, this is the client calling'
while True:
    print(f'Sending data: {send_data}')
    client.sendall(send_data)
    recv_data = client.recv(1024)
    print(f'Client received response: {str(recv_data)}')
    time.sleep(2)


