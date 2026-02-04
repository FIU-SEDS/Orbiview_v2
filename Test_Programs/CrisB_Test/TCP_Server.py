from file_select import Data_File
import TCP_Client
import socket 
import threading 
import re
import random
import csv
import time

bind_ip = "0.0.0.0" #Listens to any receiving connections 
bind_port = 9999
number_of_data_requests = 0
server_task_complete = True

class TCP_Server_Setup():
    def Server_Startup(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.server.bind((bind_ip, bind_port)) 
        # we tell the server to start listening with 
        # a maximum backlog of connections set to 5 --> Might need to change later?
        self.server.listen(5) 

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
            self.Data_Request(client_socket)

        while True: 
            # client socket and address includes in server.acept()
            try:
                client, addr = self.server.accept() #--> Blocks main thread until connection is established
            except (WindowsError, OSError):
                #force clean shutdown otherwise
                self.Ensure_Clean_Shutdown()
                return #used to terminate loop and exit function entirely

            print(f"[+] Accepted connection from: {addr[0]}:{addr[1]}")
            #spin up our client thread to handle the incoming data 
            client_handler = threading.Thread(target=handle_client, args=(client,)) #This allows for multiple simultaneous clients
            client_handler.start()

            shutdown_handler = threading.Thread(target= self.Force_Shutdown, daemon = True) #This allows for shutdown to happen at any moment conditions are met
            shutdown_handler.start()

    def Data_Request(self, client_socket):
        global number_of_data_requests
        number_of_data_requests += 1

        global server_task_complete
        server_task_complete = False

        while TCP_Client.message_sent  == False:
            time.sleep(0.05) #Forces program to constantly recheck and stay put until message is sent

        initial_data_request = client_socket.recv(4096)
        print(f"[+] Received: {initial_data_request.decode()}")

        message = initial_data_request.decode()
        number_of_requested_rows = re.findall(r'\d+', message) #Will search for integers in message, but will output in an array
        self.requested_rows = int(number_of_requested_rows[0])

        if (number_of_data_requests == 1):
            self.previous_values = [] #Set previous values to nothing

        for i in range(self.requested_rows):
            self.Placeholder_Data()
            with open(self.data_file_directory, "a", newline = "") as data_file:
                self.writer = csv.writer(data_file) #Creates writer object
                self.writer.writerow(self.new_values) #Might move to later --> Writes down data figures
                client_socket.send(f"[+] incoming values for client: {self.new_values}".encode())
                time.sleep(0.15)  
        print(f"[+] Task completed: {self.requested_rows} new row(s) added") #doesnt happen immediately
        server_task_complete = True

        TCP_Client.message_sent = False

        time.sleep(1) #This is NECESSARY for server_task_complete to be identified as true on client-side
        self.Data_Request(client_socket)

        
    def Placeholder_Data(self): 
        with open(self.data_file_directory, "r", newline="") as data_file: #"r" signigies read file; will only add onto file data
            data_file.seek(0) #moves reader back to the header row
            next(data_file) #moves reader to the next line

            #Counts rows in file
            row_count = sum(1 for row in data_file)
            print(f"[+] csv data row count: {row_count}")

            self.new_values = [] #Set new values to nothing

            for header in self.headers:
                column_index = self.headers.index(header)
                if(column_index == 5):
                    random_value = row_count #This is in creating the x-axis (time-elapsed) | Might need offset?
                elif(row_count < 1):
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

        self.previous_values = self.new_values #Sets previous values to the last made set of values as to compare in data creation

    def Force_Shutdown(self):
        while TCP_Client.server_shutting_down_signal == False:
            time.sleep(0.05)
        
        try:
            self.server.close()
        except (WindowsError, OSError):
            #force clean shutdown otherwise
            self.Ensure_Clean_Shutdown()
            return

        print("[+] Server closed")

    def Ensure_Clean_Shutdown(self):
        if self.server:
            try:
                self.server.shutdown(socket.SHUT_RDWR)
            except:
                pass
        self.server.close()
        self.server = None