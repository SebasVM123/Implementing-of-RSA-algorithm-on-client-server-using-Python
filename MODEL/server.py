import socket
import threading


class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 65432
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

    def add_connection(self, connection):
        self.connections.append(connection)

    def remove_connection(self, connection):
        self.connections.remove(connection)

    def get_connections(self):
        return self.connections


class ManageServer:
    def __init__(self):
        self.server = Server()

    def listen(self):
        self.server.socket.bind((self.server.host, self.server.port))
        self.server.socket.listen(5)
        print(f'Server started on {self.server.host}:{self.server.port}')

        while True:
            connection, address = self.server.socket.accept()
            self.server.add_connection(connection)
            print(f'Connection from {address}')
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def handle_client(self, connection, address):
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
        self.server.remove_connection(connection)
        connection.close()

    def send_message(self, message):
        for connection in self.server.connections:
            connection.sendall(message.encode())

    def start_server(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()


controller = ManageServer()
controller.start_server()
while True:
    message = input('Input a message (q to close connection): ')
    if message == 'q':
        break
    controller.send_message(message)
