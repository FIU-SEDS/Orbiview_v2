from file_select import Data_File
import socket
import time
import csv

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
        self.Request_Data(5) #integer here is merely for testing

        self.client.close()

    def Request_Data(self, requested_rows):
        request_message = "[Client] " + f"requesting {requested_rows} row(s) of data"
        self.client.send(request_message.encode())
        
    