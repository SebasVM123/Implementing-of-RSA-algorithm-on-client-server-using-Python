import socket
import threading
from tkinter import *
import tkinter.ttk as tk
from tkinter import scrolledtext, Entry, Button, Label
from ttkthemes import ThemedStyle
from tkinter import font

from RSA import RSA

FORMAT = 'UTF-8'


class Server:
    def __init__(self, host, port):
        self.rsa = RSA()

        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

        self.chat_gui()

    def chat_gui(self):
        def process_message():
            message = self.message_entry.get()
            if message:
                self.type_error_label.config(text='')
                self.message_entry.delete(0, END)
                if self.clients:
                    self.type_error_label.config(text='')
                    self.messages_area.insert(END, f'[SERVER]: {message}\n')
                    data = message
                    client = self.selected_option.get()
                    if client == 'All':
                        self.broadcast_data(data)
                    else:
                        self.send_data(data, client)
                else:
                    self.type_error_label.config(text='No one online')
            else:
                self.type_error_label.config(text='You must enter a message')

        self.window = Tk()
        self.window.title('Client-Server Chat [SERVER]')
        self.window.geometry("580x510")
        self.window.resizable(False,False)
        style= ThemedStyle(self.window)
        style.set_theme("arc")

        available_fonts = font.families()
        print(available_fonts)


        self.messages_area = Text(self.window, font=("Tahoma",11))
        self.messages_area.pack(expand=True, fill=BOTH)

        self.message_entry = tk.Entry(self.window)
        self.message_entry.pack(side=LEFT, expand=True, fill=BOTH)

        self.send_btn = tk.Button(self.window, text='Send', command=process_message)
        self.send_btn.pack(side=RIGHT)

        self.type_error_label = tk.Label(self.window, text='', foreground='red')
        self.type_error_label.pack()

        options = ['All']
        self.selected_option = StringVar(self.window)
        self.selected_option.set('All')
        self.clients_combobox = tk.Combobox(self.window, textvariable=self.selected_option, values=options, state='readonly')
        self.clients_combobox.pack()

        self.start() # Crea el hilo secundario para escuchar

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        self.messages_area.insert(END, f'[SERVER STARTED ON {self.host}:{self.port}]\n')
        print(f'Server started on {self.host}:{self.port}')

        while True:
            connection, address = self.socket.accept()

            name = self.ask_name(connection)

            self.clients_combobox['values'] = ['All'] + list(self.clients.keys())
            self.messages_area.insert(END, f'[{name} connected]\n')
            print(f'Accepted connection from {address}')
            threading.Thread(target=self.handle_client, args=(name, connection)).start()

    def handle_client(self, name, connection):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                decrypted_data = self.rsa.decrypt(int(data.decode(FORMAT)))
                self.messages_area.insert(END, f'[{name}]: {decrypted_data}\n')
                print(f'Received data from {connection.getpeername()}: {decrypted_data}')
            except socket.error:
                break

        self.messages_area.insert(END, f'[{name} CLOSED THE CONNECTION]\n')
        print(f"Connection from {connection.getpeername()} closed.")
        connection.close()

    def send_data(self, data, client_name):
        connection, client_public_key = self.clients[client_name]
        encrypted_data = self.rsa.encrypt(data, client_public_key)
        connection.sendall(str(encrypted_data).encode(FORMAT))

    def broadcast_data(self, data):
        for client_connection, client_public_key in self.clients.values():
            try:
                encrypted_data = self.rsa.encrypt(data, client_public_key)
                client_connection.sendall(str(encrypted_data).encode(FORMAT))
            except socket.error as es:
                self.messages_area.insert(END, f'[FAILED TO SEND DATA]')
                print(f'Failed to send data. Error: {es}')

    def ask_name(self, connection):
        server_public_key = self.rsa.get_public_key()
        connection.sendall(f'%NAME|{server_public_key}'.encode(FORMAT))
        data = connection.recv(1024).decode(FORMAT)
        name, public_key = data.split('|')
        self.clients[name] = (connection, eval(public_key))
        return name

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()


server = Server('localhost', 5000)
server.window.mainloop()

'''import time
time.sleep(5)
server.send_data('1234500', 'Sebas')'''
