import socket
import time
import struct
import base64

class TCP_Client_Data():
    def ClientDataSetup(self):
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

        