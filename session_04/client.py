import socket
import time

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 5555

client_socket.connect((HOST, PORT))
print(f"Connected to the server at {HOST}:{PORT}\n")

# New step: Send client name when requested
server_request = client_socket.recv(1024).decode('utf-8')
print(server_request)
client_name = input("Your Name: ")
client_socket.send(client_name.encode('utf-8'))

# Receive greeting message from server
greeting = client_socket.recv(1024).decode('utf-8')
print(greeting + "\n")

# Start two-way communication
while True:
    message = input(f"{client_name}: ")
    client_socket.send(message.encode('utf-8'))

    if message.lower() == 'exit':
        print("Closing connection...")
        break

    # Wait for server’s reply
    time.sleep(0.5)
    response = client_socket.recv(1024).decode('utf-8')
    if not response:
        break
    print(f"Server: {response}")

    if response.lower() == 'exit':
        print("Server closed the connection.")
        break

    time.sleep(0.5)

client_socket.close()
print("\nConnection closed.")
