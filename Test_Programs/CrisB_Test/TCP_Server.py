from file_select import Data_File
import socket 
import threading 
import re
import random
import csv

bind_ip = "0.0.0.0" #Listens to any receiving connections 
bind_port = 9999
connection_established = False

class TCP_Server_Setup():
    def Server_Startup(self):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server.bind((bind_ip, bind_port)) 
        # we tell the server to start listening with 
        # a maximum backlog of connections set to 5 --> Might need to change later?
        server.listen(5) 

        print(f"[+] Listening on port {bind_ip} : {bind_port}")

            #client handling thread
        def handle_client(client_socket): 
            #-----Introductory communication-----
            request_finished = False

            #printing what the client sends 
            connection_request = client_socket.recv(1024) 
            print(f"[+] Recieved: {connection_request.decode()}") 
            #sending back the packet 
            client_socket.send("[Server --> Client] Ping received".encode()) 

            #-----Data Request starts-----
            initial_data_request = client_socket.recv(4096)
            print(f"[+] Received: {initial_data_request.decode()}")

            message = initial_data_request.decode()
            number_of_requested_rows = re.findall(r'\d+', message) #Will search for integers in message, but will output in an array
            self.requested_rows = int(number_of_requested_rows[0])

            self.previous_values = [] #Set previous values to nothing
            for i in range(self.requested_rows):
                self.Placeholder_Data()
                print(self.new_values)
                with open(self.data_file_directory, "a", newline = "") as data_file:
                    self.writer = csv.writer(data_file) #Creates writer object
                    self.writer.writerow(self.new_values)

            #Might be able to call new function
            #client_socket.close()                  

        while connection_established == False: 
            # client socket and address includes in server.acept()
            client, addr = server.accept() #--> Blocks main thread until connection is established
            #connection_established = True --> Remember this if we want server to close (which we might do later)

            print(f"[+] Accepted connection from: {addr[0]}:{addr[1]}")
            #spin up our client thread to handle the incoming data 
            client_handler = threading.Thread(target=handle_client, args=(client,)) #This allows for multiple simultaneous clients
            client_handler.start()

        server.close()
        print("[+] Server closed")

    def Placeholder_Data(self): 
        with open(self.data_file_directory, "r", newline="") as data_file: #"r" signigies read file; will only add onto file data
            data_file.seek(0) #moves reader back to the header row
            next(data_file) #moves to the next line

            #Counts rows in file
            row_count = sum(1 for row in data_file)
            print(f"[+] csv row count: {row_count}")

            self.new_values = [] #Set new values to nothing

            for header in self.headers:
                column_index = self.headers.index(header)

                if(row_count < 1):
                    #make initial values
                    if(column_index == 4): #if column_index is rssi
                        random_value = random.randint(-100, -50)
                    else:
                        random_value = random.randint(0, 10)
                else:
                    #determine values based on previous values
                    if(column_index == 4): #if column_index is rssi
                        random_value = self.previous_values[column_index] + random.randint(-10, 10)
                        random_value = min(random_value, -50) #prevents going over cap
                        random_value = max(random_value, -100) #prevents going under cap
                    else:
                        random_value = self.previous_values[column_index] + random.randint(0,10)

                self.new_values.append(random_value)

        self.previous_values = self.new_values
    #return an array of random numbers?
