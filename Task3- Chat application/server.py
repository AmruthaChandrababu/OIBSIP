import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.clients = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print(f"Server started on {host}:{port}")

    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message)
                except Exception as e:
                    print(f"Error broadcasting message: {e}")
                    client.close()
                    self.clients.remove(client)

    def handle_client(self, client_socket, address):
        print(f"New connection from {address}")
        self.clients.append(client_socket)
        while True:
            try:
                message = client_socket.recv(1024)
                if message:
                    print(f"{address} says: {message.decode('utf-8')}")
                    self.broadcast(message, client_socket)
                else:
                    client_socket.close()
                    self.clients.remove(client_socket)
                    break
            except Exception as e:
                print(f"Error handling message from {address}: {e}")
                client_socket.close()
                self.clients.remove(client_socket)
                break

    def start(self):
        print("Server is running...")
        while True:
            client_socket, client_address = self.server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_handler.start()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()
