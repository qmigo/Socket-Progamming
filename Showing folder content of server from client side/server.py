import socket
import threading
import os
import json

# constants

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 1024
DISCONNECTION_MSG = ';;'
FORMAT = 'utf-8' 

# making a server connection
server = socket.socket()
server.bind(ADDR)   #binding our server to address

print('[Initialising] Socket has been initialised ....')


# utility to handle clients

def handle_client(conn, addr):
    print('[New Connection]', addr, 'connected.')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECTION_MSG:
                print(addr, 'has disconnected safely.')
                connected = False

            files = handle_files(msg)
            

            print(f"[{addr}] -> The path you mentioned {msg}")

            data = json.dumps(files)    # serialising data to send a dictionary
            conn.send(bytes(data,FORMAT))

    conn.close()    # safely closing the connection

# utility to handle files name and amount 
def handle_files(path):
    file_count=0
    file_names = list()
    if path == '/':
        path = None
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file():
                    file_count = file_count + 1
                    file_names.append(entry.name)
        return {'count':file_count, 'files':file_names}
    except:
        return -1

# start function

def start():
    print(f'[Starting] Server has been running on {ADDR}')
    server.listen()
    print('[Listening] Waiting for clients') 
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))  # used threading to make handling of clients async
        thread.start()  #starting a new thread every time new clients join


start()