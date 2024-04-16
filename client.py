import socket
import threading
from tkinter import *
import tkinter.ttk as tk
from tkinter import scrolledtext, Entry, Button, Label
from ttkthemes import ThemedStyle

from RSA import RSA

FORMAT = 'UTF-8'


class Client:
    def __init__(self, host, port):
        self.rsa = RSA()
        self.server_public_key = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)

        self.name = None

        self.login_gui()

    def login_gui(self):
        def open_chat_window():
            self.chat_gui()

        def login():
            self.name = self.name_entry.get()
            if self.name:
                print(f'Bienvenido {self.name}')
                self.connect_to_server()
                print(f'Now connected to SERVER in {self.server_address}')
                self.start() # Inicia el hilo para recibir mensajes
                open_chat_window()
            else:
                self.error_label.config(text='Debes ingresar un nombre de usuario')

        self.login_window = Tk()
        self.login_window.title('Login')
        self.login_window.geometry('300x200')
        self.style= ThemedStyle(self.login_window)
        self.style.set_theme("arc")

        self.name_label = tk.Label(self.login_window, text='Username: ')
        self.name_label.pack()

        self.name_entry = tk.Entry(self.login_window)
        self.name_entry.pack()

        self.login_btn = tk.Button(self.login_window, text='Login', command=login)
        self.login_btn.pack()

        self.error_label = tk.Label(self.login_window, text='', foreground='red')
        self.error_label.pack()

    def chat_gui(self):
        def process_message():
            message = self.message_entry.get()
            if message:
                self.type_error_label.config(text='')
                self.message_entry.delete(0, END)
                self.messages_area.insert(END, f'[Me]: {message}\n')
                data = message
                self.send_data(data)
            else:
                self.type_error_label.config(text='You must be enter a message')


        self.chat_window = Toplevel()
        self.chat_window.title(f'Client-Server Chat [{self.name}]')

        self.messages_area = Text(self.chat_window, font=("Tahoma", 11))
        self.messages_area.pack(expand=True, fill=BOTH)
        self.messages_area.insert(END, f'[SERVER]: Welcome {self.name}\n')

        self.message_entry = tk.Entry(self.chat_window)
        self.message_entry.pack(side=LEFT, expand=True, fill=BOTH)

        self.send_btn = tk.Button(self.chat_window, text='Send', command=process_message)
        self.send_btn.pack(side=RIGHT)

        self.type_error_label = tk.Label(self.chat_window, text='', foreground='red')
        self.type_error_label.pack()

    def connect_to_server(self):
        self.socket.connect(self.server_address)

    def send_data(self, data):
        encrypted_data = self.rsa.encrypt(data, self.server_public_key)
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
                    self.messages_area.insert(END, f'[SERVER]: {decrypted_data}\n')
                    print(f'Received data from SERVER: {decrypted_data}')
            except socket.error:
                break

        self.messages_area.insert(END, f'[SERVER CLOSED THE CONNECTION]\n')
        print(f'SERVER closed the connection')
        self.socket.close()

    def start(self):
        receive_data_thread = threading.Thread(target=self.receive_data)
        receive_data_thread.start()


client = Client('localhost', 5000)
client.login_window.mainloop()

'''client = Client('localhost', 5000)
client.start()

import time
time.sleep(2)

client.send_data('45678')'''
