import socket
import threading

FORMAT = 'UTF-8'


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f'Server started on {self.host}:{self.port}')

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            print(f'Accepted connection from {address}')
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def handle_client(self, connection, address):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                print(f'Received data from {address}: {data.decode(FORMAT)}')
            except socket.error:
                break

        print(f"Connection from {address} closed.")
        self.connections.remove(connection)
        connection.close()

    def send_data(self, data):
        for connection in self.connections:
            try:
                connection.sendall(data.encode())
            except socket.error as e:
                print(f'Failed to send data. Error: {e}')

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()


server = Server('localhost', 5000)
server.start()
