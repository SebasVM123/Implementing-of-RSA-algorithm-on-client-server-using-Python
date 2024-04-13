import socket
import threading

FORMAT = 'utf-8'


class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.name = self.login()

    @staticmethod
    def login():
        name = input('Enter your name: ')
        return name

    def send_data(self, data):
        self.socket.sendall(data.encode(FORMAT))

    def receive_data(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                print(f'Received data from SERVER: {data.decode(FORMAT)}')
            except socket.error:
                break

        print(f'SERVER closed the connection')
        self.socket.close()

    def start(self):
        receive_data_thread = threading.Thread(target=self.receive_data)
        receive_data_thread.start()


client = Client('localhost', 5000)
client.start()
