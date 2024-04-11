import socket
import threading


class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 65432
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f'Server started on {self.host}:{self.port}')

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            print(f'Connection from {address}')
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def handle_client(self, connection, address):
        with connection:
            while True:
                try:
                    data = connection.recv(1024)
                    if not data:
                        break
                    print(f'Data received from {address}: {data.decode()}')
                    connection.sendall('Message received successfully'.encode())
                except socket.error:
                    break

            print(f'Connection from {address} closed')
            self.connections.remove(connection)

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()


server = Server()
server.start()
