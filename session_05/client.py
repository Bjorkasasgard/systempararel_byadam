import socket
import threading

# Terima pesan dari server
def receive_from_server(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("Koneksi dengan server terputus.")
            client_socket.close()
            break

# Jalankan client
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))

    threading.Thread(target=receive_from_server, args=(client,), daemon=True).start()

    while True:
        msg = input("")
        if msg.lower() == "exit":
            print("Keluar dari obrolan.")
            client.close()
            break
        client.send(msg.encode('utf-8'))

if __name__ == "__main__":
    start_client()
