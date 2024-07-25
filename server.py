import socket
import threading

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'  # Localhost
port = 12345  # Changed port

try:
    server.bind((host, port))
except socket.error as e:
    print(f"Binding failed. Error: {str(e)}")
    exit()

server.listen()
print('Server is listening...')

clients = []
nicknames = []

# Broadcast message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle individual client connection
def handle_client(client):
    while True:
        try:
            # Receive message
            message = client.recv(1024)
            broadcast(message)
        except:
            # Remove and close client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# Receive connections
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        # Request and store nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        # Start handling thread for client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
