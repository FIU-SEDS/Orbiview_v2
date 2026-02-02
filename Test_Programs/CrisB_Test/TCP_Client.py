from file_select import Data_File
import TCP_Server
import socket
import time
import csv

message_sent = False
server_shutting_down_signal = False

class TCPClient():
    def Client_Setup(self):
        time.sleep(1) #pauses time for 1 second
        target_host = "127.0.0.1" #local host
        target_port = 9999

        #Creating socket object
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Initial communication
        #connecting the client
        self.client.connect((target_host, target_port))
        #sending the data
        self.client.send("[Client] Establishing connection...".encode())
        #receiving the data
        response = self.client.recv(4096)
        print(response.decode())

        #Request data here
        self.Request_Data(self.Prompt_User(False)) #integer here is merely for testing --> Prompt user?

    def Request_Data(self, requested_rows):
        global message_sent
        message_sent = False

        request_message = "[Client] " + f"requesting {requested_rows} row(s) of data"

        try:
            self.client.send(request_message.encode())
        except (OSError, WindowsError):
            #socket is gone or invalid, force clean shutdown
            if self.client:
                try:
                    self.client.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass
                self.client.close()
                self.client = None
            return #exit function and loop

        message_sent = True

        for i in range(requested_rows):
            data_response = self.client.recv(4096)
            print(data_response.decode())
        
        print("[Client] All data figures received")

        while TCP_Server.server_task_complete == False:
            time.sleep(0.05) #Ensures next method won't start until server finishes data task

        self.Request_Data(self.Prompt_User(True)) #Prompt user again for more rows --> If yes, creates loop
        #perhaps here we need to create a data response array and have a return value????

    def Prompt_User(self, repeated_entry):
        if repeated_entry:
            inputting_response = True
            
            while inputting_response:
                more_rows = input("Do you want more rows for data figures? Y/N")
                clean_input_of_rows = more_rows.lower().strip()

                if clean_input_of_rows == "y" or clean_input_of_rows == "yes":
                    #Communicate with server to go again
                    #self.client.send("Requesting further data entries...".encode())
                    inputting_response = False
                elif clean_input_of_rows == "n" or clean_input_of_rows == "no":
                    try:
                        self.client.close()
                    except (OSError, WindowsError):
                        if self.client:
                            try:
                                self.client.shutdown(socket.SHUT_RDWR)
                            except:
                                pass
                            self.client.close()
                            self.client = None
                    global server_shutting_down_signal
                    server_shutting_down_signal = True #Triggers server shutdown process
                    return #Exits the function entirely
                else:
                    print("That's not a valid response. Try again", flush=True)
            
        inputting_number = True

        while inputting_number:
            requested_rows = input("How many data rows do you want?\n")

            try:
                number_of_requested_rows = int(requested_rows)
                if number_of_requested_rows >= 1:
                    inputting_number = False
                else:
                    print("Number out of range. Try again.")
            except ValueError:
                print("That's not a valid number. Try again.")

        return number_of_requested_rows