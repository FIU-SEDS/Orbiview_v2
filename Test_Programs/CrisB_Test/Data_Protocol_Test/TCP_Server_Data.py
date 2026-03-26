import socket 
import threading 
import struct
import base64
import random
import time

bind_ip = "0.0.0.0" 
bind_port = 9999
dataPending  = False

class TCP_Server_Data():
    def Server_Data_Setup(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((bind_ip, bind_port)) 
        # we tell the server to start listening with 
        # a maximum backlog of connections set to 5
        server.listen(5) 

        print(f"[+] Listening on port {bind_ip} : {bind_port}")                            

        #client handling thread
        def handle_client(client_socket): 
            #printing what the client sends 
            request = client_socket.recv(1024) 
            print(f"[+] Recieved: {request.decode()}") 
            #sending back the packet 
            client_socket.send("Ping recevied".encode()) 
            
            self.Data_Generation(client_socket)
            
            #client_socket.close() --> closes connection with client?


        while True: 
            # When a client connects we receive the 
            # client socket into the client variable, and 
            # the remote connection details into the addr variable
            client, addr = server.accept() 
            print(f"[+] Accepted connection from: {addr[0]}:{addr[1]}")
            #spin up our client thread to handle the incoming data 
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start() 

    def Data_Generation(self, client_socket):
        
        client_socket.send("Initiating server data generation...".encode())
        time.sleep(0.5)

        #will later change to random values
        packets = [
            self.Build_Packets(0, 23.5, 55.1, 1013.25, 150.0),       # BME
            self.Build_Packets(1, 0.01, -0.02, 9.81, 0.5, -0.3, 0.1), # IMU
            self.Build_Packets(2, 28.538336, -81.379234),               # GPS
            self.Build_Packets(3, 274.5),                               # MAG
        ]

        #Telling client how many packets are being received --> Will be changed later as amount varies
        num_Packets = len(packets)
        client_socket.send(f"{num_Packets} packets are being sent".encode())

        #Would send packets to client
        for pkt in packets:
            client_socket.send(pkt)
            global dataPending
            dataPending = True #condition to seperate packets
            while dataPending:
                time.sleep(0.1)

    def Build_Packets(self, packet_id, *floats):
        # Pack the packet ID as 1 byte
        id_byte = struct.pack('<B', packet_id)
    
        # Pack all floats, each is 4 bytes
        float_bytes = struct.pack(f'<{len(floats)}f', *floats)
    
        # Combine into raw bytes
        raw_bytes = id_byte + float_bytes
    
        # Base64 encode the raw bytes
        b64 = base64.b64encode(raw_bytes)
    
        # Prefix with 3-digit ASCII length, zero-padded (e.g., 28 -> b'028')
        prefix = f'{len(b64):03d}'.encode('ascii')
    
        return prefix + b64