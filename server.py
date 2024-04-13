import socket
import threading

from RSA import RSA

FORMAT = 'UTF-8'


class Server:
    def __init__(self, host, port):
        self.rsa = RSA()

        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.clients = {}

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f'Server started on {self.host}:{self.port}')

        while True:
            connection, address = self.socket.accept()

            self.ask_name(connection)
            self.connections.append(connection)
            print(f'Accepted connection from {address}')
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def handle_client(self, connection, address):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                decrypted_data = self.rsa.decrypt(int(data.decode(FORMAT)))
                print(f'Received data from {address}: {decrypted_data}')
            except socket.error:
                break

        print(f"Connection from {address} closed.")
        self.connections.remove(connection)
        connection.close()

    def send_data(self, data, client_name):
        '''for connection in self.connections:
            try:
                connection.sendall(data.encode())
            except socket.error as e:
                print(f'Failed to send data. Error: {e}')'''
        connection, client_public_key = self.clients[client_name]
        encrypted_data = self.rsa.encrypt(int(data), client_public_key)
        connection.sendall(str(encrypted_data).encode(FORMAT))

    def ask_name(self, connection):
        server_public_key = self.rsa.get_public_key()
        connection.sendall(f'%NAME|{server_public_key}'.encode(FORMAT))
        data = connection.recv(1024).decode(FORMAT)
        name, public_key = data.split('|')
        self.clients[name] = (connection, eval(public_key))

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()


server = Server('localhost', 5000)
server.start()

'''import time
time.sleep(20)
server.send_data('4567')'''
import time
time.sleep(5)
server.send_data('1234500', 'Sebas')
