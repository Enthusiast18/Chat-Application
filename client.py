'''
This module defines the behaviour of a client in your Chat Application
'''
from base64 import encode
import sys
import getopt
import socket
import random
from threading import Thread
import os
import util
import time


'''
Write your code inside this class. 
In the start() function, you will read user-input and act accordingly.
receive_handler() function is running another thread and you have to listen 
for incoming messages in this function.
'''


class Client:
    '''
    This is the main Client Class. 
    '''

    def __init__(self, username, dest, port):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(None)
        self.name = username
        self.connected = True
        
        self.sock.connect((self.server_addr, self.server_port))

    def start(self):
        '''
        Main Loop is here
        Start by sending the server a JOIN message.
        Waits for userinput and then process it
        '''
        message_to_send = "join " + self.name
        self.sock.send(message_to_send.encode('UTF-8'))
        
        
        message = ""
        while self.connected:
    
            message = input()
            message_keys = message.split()
            
            if(self.connected == True):
                if(message == "list" and len(message_keys) == 1):
                    message_to_send = "request_users_list"
                    self.sock.send(message_to_send.encode('UTF-8'))
            
                elif(message == "quit" and len(message_keys) == 1):
                    print("quitting")
                    self.connected = False
                    message_to_send = "disconnect"
                    self.sock.send(message_to_send.encode('UTF-8'))
                    break
                
                elif(message_keys[0] == "msg" and len(message_keys) > 2):
                    message_to_send = "send_message " + " ".join(message_keys[1:])
                    self.sock.send(message_to_send.encode('UTF-8'))
                
                elif(message_keys[0] == "file"and len(message_keys) > 3):
                    if(os.path.isfile(message_keys[-1]) and int(message_keys[1]) == len(message_keys)-3):
                        f_name = message_keys[-1]
                        file = open(f_name, 'r')
                        send_file = file.read()
                        message_to_send = "send_file " + " ".join(message_keys[1:]) + " " + send_file
                        file.close()
                        self.sock.send(message_to_send.encode('UTF-8'))
                    else:
                        print("no such file in directory")
                    
                elif(message == "help"):
                    print("\"list\": print list of all online users")
                    print("\"msg <num_of_users> <list_of_users> <message>\": send message to the list of users specified")
                    print("\"file <num_of_user> <list_of_users> <file>\": send file to the list of users specified")
                    print("\"quit\": disconnect from server")
                    print("\"help\": print this help")
                
                else:
                    print("incorrect userinput format")
                    
                
        self.sock.close()
        quit()
        
        # raise NotImplementedError

    def receive_handler(self):
        '''
        Waits for a message from server and process it accordingly
        '''
        while self.connected:
            mess = self.sock.recv(4096)
            mess = mess.decode('UTF-8')
            message_split = mess.split()
            
            if(mess == "err_server_full"):
                print("disconnected: server full")
                self.connected = False
            elif(mess == "err_username_unavailable"):
                print("disconnected: username not available")
                self.connected = False
            elif(mess == "err_unknown_message"):
                print("disconnected: server received an unknown command")
                self.connected = False
            elif(message_split[0] == "forward_message"):
                temp = " ".join(message_split[2:])
                print("msg: ", message_split[1], ": ", temp, sep='')
            elif(message_split[0] == "response_users_list"):
                temp = "list: "+ " ".join(message_split[2:])
                print(temp)
            elif(message_split[0] == "forward_file"):
                temp = " ".join(message_split[3:])
                file_name = self.name + "_" + message_split[2]
                f = open(file_name, "w")
                f.write(temp)
                f.close()
                print("file: ", message_split[1], ": ", message_split[2], sep='')
            else:
                print(mess)

        # raise NotImplementedError


# Do not change this part of code
if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our Client module completion
        '''
        print("Client")
        print("-u username | --user=username The username of Client")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-h | --help Print this help")
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "u:p:a", ["user=", "port=", "address="])
    except getopt.error:
        helper()
        exit(1)

    PORT = 15000
    DEST = "localhost"
    USER_NAME = None
    for o, a in OPTS:
        if o in ("-u", "--user="):
            USER_NAME = a
        elif o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a

    if USER_NAME is None:
        print("Missing Username.")
        helper()
        exit(1)

    S = Client(USER_NAME, DEST, PORT)
    try:
        # Start receiving Messages
        T = Thread(target=S.receive_handler)
        T.daemon = True
        T.start()
        # Start Client
        S.start()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
