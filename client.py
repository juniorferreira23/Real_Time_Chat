import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from time import sleep
import sys

class Client:
    def __init__(self, host: str = 'localhost', port: int = 5556):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.running = True

        main_window = tk.Tk()
        main_window.withdraw()
        self.name = simpledialog.askstring('Name', 'Enter your name:', parent=main_window)
        self.chat = simpledialog.askstring('Chat', 'Enter the chat:', parent=main_window)

        self.thread = threading.Thread(target=self.connect_chat, daemon=True)
        self.thread.start()

        self.chat_window()

    def connect_chat(self):
        try:
            while self.running:
                try:
                    response = self.sock.recv(1024).decode()
                    if not response:
                        break

                    if response == 'Chat':
                        self.sock.send(self.name.encode())
                        sleep(1)
                        self.sock.send(self.chat.encode())
                    else:
                        self.update_chat(response)
                except socket.error:
                    break
        except Exception as e:
            print(f'Erro em handle: {e}')
        finally:
            self.sock.close()

    def update_chat(self, message):
        if self.chat_window.winfo_exists():
            self.chat_window.after(0, lambda: self.box_text.insert('end', message))

    def chat_window(self):
        self.chat_window = tk.Tk()
        self.chat_window.geometry('600x600')
        self.chat_window.title('Chat')

        self.box_text = tk.Text(self.chat_window)
        self.box_text.place(relx=0.04, rely=0.01, width=550, height=400)

        self.input_message = tk.Entry(self.chat_window)
        self.input_message.place(relx=0.04, rely=0.7, width=440, height=30)

        self.btn_send = tk.Button(self.chat_window, text='Send', command=self.send_message)
        self.btn_send.place(relx=0.79, rely=0.7, width=100, height=30)

        self.chat_window.protocol('WM_DELETE_WINDOW', self.close_chat)

        self.chat_window.mainloop()

    def send_message(self):
        message = self.input_message.get()
        if message.strip():
            self.sock.send(message.encode())
            self.input_message.delete(0, 'end')

    def close_chat(self):
        self.running = False
        self.sock.send(b'EXIT')
        self.sock.close()
        self.chat_window.destroy()
        sys.exit()


if __name__ == '__main__':
    client = Client()
