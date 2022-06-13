'''
This module defines the behaviour of server in your Chat Application
'''
import sys
import getopt
import socket
import util
import threading


class Server:
    '''
    This is the main Server Class. You will to write Server code inside this class.
    '''
    

    def __init__(self, dest, port):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(None)
        self.sock.bind((self.server_addr, self.server_port))
        self.client_infos = []
        self.client_names = []

    def start(self):
        '''
        Main loop.
        continue receiving messages from Clients and processing it
        '''
        self.sock.listen(util.MAX_NUM_CLIENTS)
        
        while True:
            info = self.sock.accept()
            connected = True
            
            if(len(self.client_names) >= util.MAX_NUM_CLIENTS):
                send_message = "err_server_full"
                info[0].send(send_message.encode('UTF-8'))
                print("disconnected: server full")
                connected = False
                
            else:
                recv_message = info[0].recv(4096)
                recv_message = recv_message.decode('UTF-8')
                username = recv_message.split()
                if(username[1] in self.client_names):
                    send_message = "err_username_unavailable"
                    info[0].send(send_message.encode('UTF-8'))
                    print("disconnected: username not available")
                    connected = False
                else:
                    self.client_infos.append(info)
                    self.client_names.append(username[1])
                    print("join:", username[1])
                
            threading.Thread(target=self.client_handler, args=(info, connected)).start()
            
    def client_handler(self, info, connection):
        message_send = ""
        message_recv = ""
        
        while(connection):
            message_recv = info[0].recv(4096)
            message_recv = message_recv.decode('UTF-8')
            message_keys = message_recv.split()
            index = self.client_infos.index(info)
            name = self.client_names[index]
            
            if(message_recv == "request_users_list"):
                list_send = self.client_names.copy()
                list_send.sort()
                print("request_users_list:", name)
                message_send = "response_users_list " + str(len(list_send)) + " " + " ".join(list_send)
                info[0].send(message_send.encode('UTF-8'))
                
            elif(message_keys[0] == "send_message"):
                
                if(not message_keys[1].isnumeric() or (int(message_keys[1]) > (len(message_keys) - 2))):
                    message_send = "err_unknown_message"
                    info[0].send(message_send.encode('UTF-8'))
                    self.client_infos.remove(info)
                    self.client_names.remove(name)
                    connection = False
                    print("disconnected:", name, "sent unknown command")
                    break
                else:
                    print("msg:", name)
                    to_send = []
                    for i in range(2, int(message_keys[1])+2):
                        to_send.append(message_keys[i])
                    to_send = list(set(to_send))
                        
                    message_send = "forward_message " + name + " " + " ".join(message_keys[2+int(message_keys[1]):])
                    
                    for clients in to_send:
                        if(clients not in self.client_names):
                            print("msg:", name, "to non-existent user", clients)
                        else:
                            rcv_index = self.client_names.index(clients)
                            receiver = self.client_infos[rcv_index]
                            receiver[0].send(message_send.encode('UTF-8'))
                            
            elif(message_keys[0] == "send_file"):
                if(not message_keys[1].isnumeric()):
                    message_send = "err_unknown_message"
                    info[0].send(message_send.encode('UTF-8'))
                    self.client_infos.remove(info)
                    self.client_names.remove(name)
                    connection = False
                    print("disconnected:", name, "sent unknown command")
                    break
                else:
                    num_recv = int(message_keys[1])
                    print("file:", name)
                    to_send_file = []
                    for i in range (2, num_recv+2):
                        to_send_file.append(message_keys[i])
                    to_send_file = list(set(to_send_file))
                    
                    message_send = "forward_file " + name + " " + message_keys[2+ num_recv] + " " + " ".join(message_keys[3+num_recv:])
                    for rec in to_send_file:
                        if(rec not in self.client_names):
                            print("file:", name, "to non-existent user", rec)
                        else:
                            rcv_index = self.client_names.index(rec)
                            receiver = self.client_infos[rcv_index]
                            receiver[0].send(message_send.encode('UTF-8'))
                
            elif(message_recv == "disconnect"):
                info[0].close()
                self.client_infos.remove(info)
                self.client_names.remove(name)
                print("disconnected:", name)
                break

        # raise NotImplementedError

# Do not change this part of code


if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our module completion
        '''
        print("Server")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-h | --help Print this help")

    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "p:a", ["port=", "address="])
    except getopt.GetoptError:
        helper()
        exit()

    PORT = 15000
    DEST = "localhost"

    for o, a in OPTS:
        if o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a

    SERVER = Server(DEST, PORT)
    try:
        SERVER.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
