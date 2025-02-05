import socket
import threading

data_payload = 1024
chats = {}

def handle_error(message, client, chat=None):
    print(message)
    if chat and chat in chats and client in chats[chat]:
        chats[chat].remove(client)
        if not chats[chat]:
            del chats[chat]
    
    try:
        client.shutdown(socket.SHUT_RDWR) 
    except:
        pass
    finally:
        client.close()

def broadcast(chat: str, message: str):
    if chat in chats:
        for client in chats[chat][:]:
            try:
                client.send(message.encode())
            except:
                handle_error(f'Error sending message to {client}', client, chat)

def handle_messages(name: str, chat: str, client: socket.socket) -> None:
    try:
        while True:
            message = client.recv(data_payload)
            if not message or message == b'EXIT':
                break
            message = f'{name}: {message.decode()}\n'
            broadcast(chat, message)
    except socket.error as e:
        handle_error(f'Erro socket in handle_messages: {e}', client, chat)
    except Exception as e:
        handle_error(f'Erro in handle_messages: {e}', client, chat)
    finally:
        handle_error(f'{name} left the chat {chat}', client, chat)

def run_server(host: str = 'localhost', port: int = 5556) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    print(f'Server started successfully on port: {port}')
    
    while True:
        try:
            client, address = sock.accept()
            print(f'Connection to client {address} established successfully')            
            client.send(b'Chat')

            name = client.recv(data_payload).decode().strip()
            chat = client.recv(data_payload).decode().strip()

            if not name or not chat:
                handle_error('Invalid name or chat', client)
                continue

            if chat not in chats:
                chats[chat] = []
            chats[chat].append(client)

            broadcast(chat, f'{name} entered the room\n')

            thread = threading.Thread(target=handle_messages, args=(name, chat, client))
            thread.start()
        except socket.error as e:
            print(f'Erro socket: {e}')
        except Exception as e:
            print(f'Erro except: {e}')

if __name__ == '__main__':
    run_server()
