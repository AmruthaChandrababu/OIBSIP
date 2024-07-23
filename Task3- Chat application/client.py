import socket
import threading
class ChatClient:
    def __init__(self, host='127.0.0.1', port=5000):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.username = input("Enter your username: ")

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    print(message)
                else:
                    self.client.close()
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.client.close()
                break

    def send_messages(self):
        while True:
            message = input()
            if message:
                self.client.send(f"{self.username}: {message}".encode('utf-8'))

    def start(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
        
        send_thread = threading.Thread(target=self.send_messages)
        send_thread.start()

if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.start()
