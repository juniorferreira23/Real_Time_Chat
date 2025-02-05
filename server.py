"""
1 - Iniciar o servidor socket [x]
2 - Receber requisições [x]
3 - Colocar os clientes em uma sala [x]
4 - Fazer uma funcionalidade para ficar escutando os clientes nas salas [x]
5 - Encaminhar a mensagem de um cliente em determinada sala para todos os clientes na mesma sala [x]
"""

import socket
import threading

data_payload = 1024
chats = {}

def handle_error(message, chat, client):
    chats[chat].remove(client)
    client.close()
    

def broadcast(chat:str, message:str):
    for client in chats[chat]:
        client.send(message.encode())


def handle_menssages(name:str, chat:str, client:socket.socket) -> None:
    try:
        while True:
            message = client.recv(data_payload)
            if message:
                message = message.decode()
                message = f'{name}: {message}\n'
                broadcast(chat, message) 
    except socket.error as e:
        handle_error(f'Erro socket em handle: {e}', chat, client)
    except Exception as e:
        handle_error(f'Erro em handle: {e}', chat, client)
        

def run_server(host:str='localhost', port:int=8082) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    print(f'Servidor iniciado com sucesso na porta: {port}')
    
    while True:
        try:        
            client, address = sock.accept()
            print(f'Conexão com o cliente({address}) estabelecida com sucesso')            
            client.send(b'Sala e nome')            
            response = client.recv(data_payload).decode()
            if response:
                name, chat = response.split('|')            
                if chat not in chats:
                    chats[chat] = []
                chats[chat].append(client)
                client.send(f'{name} entrou na sala\n'.encode())                
                thread = threading.Thread(target=handle_menssages, args=(name, chat, client))
                thread.start()                        
        except socket.error as e:
            handle_error(f'Erro socket: {e}', chat, client)            
        except Exception as e:
            handle_error(f'Erro except: {e}', chat, client)            

    
if __name__ == '__main__':
    run_server()
        
