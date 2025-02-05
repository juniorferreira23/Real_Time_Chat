"""
1 - Enviar o nome e a sala
2 - Enviar mensagens no chat de conversa
"""

import socket
import threading
from time import sleep

def handler_server(sock):
    try:
        count = 0
        while True:
            response = sock.recv(1024).decode()
            if response == 'Sala e nome':
                sock.send(b'Gabriel|Jogos')
            else:
                print(response)
                sock.send(b'ola mundo')
                sleep(10)
                if count >= 3:
                    sock.close()
                    break
                count += 1
    except socket.error as e:
        print(f'Erro socket em handle: {e}')
    except Exception as e:
        print(f'Erro em handle: {e}')
 


def run_client(host:str='localhost', port:int=8082):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        thread = threading.Thread(target=handler_server, args=(sock,))
        thread.start()
    except socket.error as e:
        print(f'Erro socket: {e}')
    except Exception as e:
        print(f'Erro: {e}')
    
        
            
if __name__ == '__main__':
    run_client()