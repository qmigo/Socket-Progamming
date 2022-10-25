import socket
import json


# all the constants

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())   # gets the localhost of our system
# SERVER = '127.0.0.1'  # will change upon different servers
ADDR = (SERVER, PORT)
HEADER = 1024
DISCONNECTION_MSG = ';;'
FORMAT = 'utf-8' 

client = socket.socket()  #creating a client connection using default parameters for IF_NET and SOCK_STREAM
client.connect(ADDR)    #connecting to the server address

# a utility to send message with ability to calculate the header buffer automatically making it optimised
def send(message):
    msg = message.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(msg)

# set of instructions
print('\n   Instructions to use : \n')
print('1.  / will give you files present in the folder in which server.py is running.\n')
print('2.  Give absolute addresses in the input so it can return files count . for example ( C:\\Users\\admin\\Desktop )\n')
print('3.  use ../ to go one folder back\n')
# main utility  to connect with server and interact with it.

while True:
    msg = input("Enter absolute path of directory to search for files : ")
    
    if msg == DISCONNECTION_MSG:
        print("Closing your connection !!!")
        send(msg)
        break
    send(msg)

    data = client.recv(1024).decode(FORMAT)     #recieves the data in string format
    files = json.loads(data)    # parse the data into JSON object (here we used a dictionary)
    
    
    if files == -1:     # if the path was not found (this case is different then empty directory)
        print('Path is not found in Server')

    else :
        print('The file count only at ',msg, '=' ,files['count'])    #printing the files count in folder
        if files['count']== 0:
            print('Empty Directory. Add some files to see the change')  # printing the list of files only
        else :
            print("The files are :")
            i = 1
            for file in files['files']:
                print(f'{i}. {file}')
                i = i+1
    
