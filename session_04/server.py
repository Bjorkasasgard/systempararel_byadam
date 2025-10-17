import socket
import time

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 5555

server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server is running on {HOST}:{PORT}")
print("Waiting for a client to connect...\n")

while True:
    try:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected to client: {client_address}\n")

        # Ask for client's name
        client_socket.send("Please enter your name: ".encode('utf-8'))
        client_name = client_socket.recv(1024).decode('utf-8')
        print(f"New client joined with name: {client_name}")
        client_socket.send(f"Hello {client_name}! Welcome to the server 👋".encode('utf-8'))

        # Two-way communication with the client
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"Connection with {client_name} was lost.\n")
                break

            print(f"{client_name}: {message}")

            if message.lower() == 'exit':
                print(f"{client_name} has left the server.\n")
                break

            # Server's reply
            time.sleep(0.5)
            response = input("Server: ")
            client_socket.send(response.encode('utf-8'))

            if response.lower() == 'exit':
                print("Server has closed this chat session.\n")
                break

        # Close connection with the client after the session ends
        client_socket.close()
        print("Waiting for the next client...\n")

    except KeyboardInterrupt:
        print("\nServer manually stopped.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        continue

# Close the server after exiting the loop
server_socket.close()
print("Server has been completely shut down.")
