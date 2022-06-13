# Chat-Application
---------------------------------------------------------------
Run server file in the command line using the following format: 
python server.py -p <port_number>
---------------------------------------------------------------
  
  
---------------------------------------------------------------
Run client file in the command line using the following format:
python client.py -p <server_port_number> -u <username>
---------------------------------------------------------------
  
---------------------------------------------------------------
Following are the functionalities of the chat app:
  
  1- Send Message to a user |
    Message format: 
       msg <number_of_recepients> <list_of_recepients> <message>
  
  2- Request list of users |
    Message format:
        list
  
  3- Send files to a user |
    Message format:
        file <number_of_recpients> <list_of_recepients> <file_names>
  
  4- Disconnect from chat app |
    Message format:
         quit
  
  5- Show help |
    Message format:
        help
