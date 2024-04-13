import socket
import threading

from RSA import RSA

FORMAT = 'utf-8'


class Client:
    def __init__(self, host, port):
        self.rsa = RSA()
        self.server_public_key = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = self.login()
        self.socket.connect((host, port))
        print(f'Now connected to SERVER in {host}:{port}')

    @staticmethod
    def login():
        name = input('Enter your name: ')
        return name

    def send_data(self, data):
        encrypted_data = self.rsa.encrypt(int(data), self.server_public_key)
        self.socket.sendall(str(encrypted_data).encode(FORMAT))

    def receive_data(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break

                if not self.server_public_key and data.decode(FORMAT)[:5] == '%NAME':
                    self.server_public_key = eval(data.decode(FORMAT).split('|')[1])

                    client_public_key = self.rsa.get_public_key()
                    self.socket.sendall(f'{self.name}|{client_public_key}'.encode(FORMAT))
                else:
                    decrypted_data = self.rsa.decrypt(int(data.decode(FORMAT)))
                    print(f'Received data from SERVER: {decrypted_data}')
            except socket.error:
                break

        print(f'SERVER closed the connection')
        self.socket.close()

    def start(self):
        receive_data_thread = threading.Thread(target=self.receive_data)
        receive_data_thread.start()


client = Client('localhost', 5000)
client.start()

import time
time.sleep(2)

client.send_data('45678')
