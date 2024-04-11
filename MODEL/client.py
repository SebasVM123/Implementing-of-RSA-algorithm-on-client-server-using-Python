import socket
import threading

HOST = '127.0.0.1'
PORT = 65432


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class ManageClient:
    def __init__(self):
        self.client = Client()

    def connect_to_server(self, host, port):
        self.client.socket.connect((host, port))
        threading.Thread(target=self.receive_messages).start()

    def send_message(self, message):
        self.client.socket.sendall(message.encode())

    def receive_messages(self):
        while True:
            data = self.client.socket.recv(1024).decode()
            print(data)
            if not data:
                print('Connection with server closed')
                self.close_connection()
                break

    def close_connection(self):
        self.client.socket.close()


controller = ManageClient()
controller.connect_to_server(HOST, PORT)
while True:
    message = input('Input a message (q to close connection): ')
    if message == 'q':
        break
    controller.send_message(message)

