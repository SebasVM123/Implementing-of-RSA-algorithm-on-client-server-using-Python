import socket

HOST = '127.0.0.1'
PORT = 65432


class Client:
    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.client:
            self.client.connect((HOST, PORT))

            message = 'Hello world 2'
            self.client.sendall(message.encode())

            data = self.client.recv(1024).decode()
            print(data)


client = Client()
