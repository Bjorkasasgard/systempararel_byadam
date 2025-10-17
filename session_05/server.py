import socket
import threading

clients = {}  # Dictionary untuk menyimpan semua client yang terhubung  key = socket, value = nama client

# Kirim pesan ke semua client
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                del clients[client]

# Fungsi untuk menangani tiap client di thread terpisah
def handle_client(client_socket, addr):
    try:
        # Minta nama client setelah terhubung
        client_socket.send("Masukkan nama kamu: ".encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8').strip()
        clients[client_socket] = name

        print(f"[TERHUBUNG] {name} ({addr}) telah terhubung.")
        broadcast(f"[SERVER] {name} telah bergabung ke obrolan.")

        # Loop untuk terus menerima pesan dari client
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            full_message = f"[{name}] {message}"
            print(full_message)
            broadcast(full_message, sender_socket=client_socket)
    except:
        pass
    # Jika client keluar atau error
    finally:
        print(f"[PUTUS] {clients.get(client_socket, addr)} terputus.")
        broadcast(f"[SERVER] {clients.get(client_socket, addr)} telah keluar.")
        del clients[client_socket]
        client_socket.close()

# Jalankan server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))
    server.listen()

    print("[SERVER AKTIF] Menunggu koneksi client...\n")

    # Thread untuk kirim broadcast manual dari server
    def send_broadcast():
        while True:
            msg = input("")
            broadcast(f"[SERVER]: {msg}")

    threading.Thread(target=send_broadcast, daemon=True).start()

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
