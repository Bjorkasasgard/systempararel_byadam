import socket #import module (comunication)
import threading #import module broadcast

clients = []
client_names = []
server_running = True  # Flag control

# boradcast function
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

# Fungsi untuk menangani tiap client
def handle_client(client_socket, client_address):
    global server_running
    try:
        client_socket.send("Please enter your name: ".encode('utf-8'))
        client_name = client_socket.recv(1024).decode('utf-8').strip()
        client_names.append(client_name)
        clients.append(client_socket)

        print(f"[NEW CONNECTION] {client_name} from {client_address}")
        client_socket.send(f"Hello {client_name}! Welcome to the chat room!".encode('utf-8'))
        broadcast(f"{client_name} has joined the chat!", client_socket)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            if message.lower() == 'exit':
                print(f"[DISCONNECT] {client_name} left the chat.")
                broadcast(f"{client_name} has left the chat.", client_socket)
                break

            print(f"{client_name}: {message}")
            broadcast(f"{client_name}: {message}", client_socket)

    except:
        pass
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

# Fungsi agar server juga bisa kirim pesan
def server_send():
    global server_running
    while server_running:
        try:
            message = input("Server: ")
            if message.lower() == 'exit':
                broadcast("Server has closed the chat. Goodbye everyone!")
                print("\n[SERVER SHUTDOWN] All clients will be disconnected...")
                for client in clients:
                    client.close()
                server_running = False
                break
            else:
                print(f"Server: {message}")
                broadcast(f"Server: {message}")
        except:
            break

# Fungsi utama server
def start_server():
    global server_running
    HOST = '127.0.0.1'
    PORT = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"🚀 Server running on {HOST}:{PORT}")
    print("Type your message directly here to chat as Server.")
    print("Type 'exit' to shut down the server.\n")

    # Thread untuk meng-handle input dari server
    threading.Thread(target=server_send, daemon=True).start()

    try:
        while server_running:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")  # -2 = exclude main + input thread
    except KeyboardInterrupt:
        print("\nServer manually stopped.")
    finally:
        server_socket.close()
        print("Server has been completely shut down.")

if __name__ == "__main__":
    start_server()
