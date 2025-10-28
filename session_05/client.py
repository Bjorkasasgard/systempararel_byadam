import socket #import module socket
import threading
import sys

def receive_messages(client_socket):
   
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n{message}")
        except:
            print("\n⚠️ Disconnected from server.")
            client_socket.close()
            break

def send_messages(client_socket):
    """Mengirim pesan ke server."""
    while True:
        message = input("")
        client_socket.send(message.encode('utf-8'))
        if message.lower() == 'exit':
            print("You have left the chat.")
            client_socket.close()
            sys.exit()  # Tutup program client tanpa ganggu client lain

def start_client():
    HOST = '127.0.0.1'
    PORT = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Dapatkan permintaan nama
    name_request = client_socket.recv(1024).decode('utf-8')
    print(name_request)
    name = input("Your Name: ")
    client_socket.send(name.encode('utf-8'))

    # Terima pesan sambutan
    welcome = client_socket.recv(1024).decode('utf-8')
    print(f"\n{welcome}\n")
    print("You can now start chatting. Type 'exit' to leave.\n")

    # Mulai dua thread: satu untuk kirim, satu untuk terima
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    start_client()
