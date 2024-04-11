import socket

HOST = '127.0.0.1'
PORT = 65432


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_data(self):
        while True:
            message = input('Input a message (q to close connection): ')
            if message == 'q':
                break
            self.socket.sendall(message.encode())
            data = self.socket.recv(1024)
            print(data.decode())

    def start(self, host, port):
        with self.socket:
            self.socket.connect((host, port))
            self.send_data()


client = Client()
client.start('127.0.0.1', 65432)
