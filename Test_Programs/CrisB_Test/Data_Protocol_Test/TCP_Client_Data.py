import socket
import time
import TCP_Server_Data
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
        print(f"[Client]: {response.decode()}")

        #Gets confirmation server is generating data
        print(f"{self.client.recv(4096).decode()}")

        #Gets told by server amount of packets being sent
        message = self.client.recv(1024).decode()  # "# packets are being sent"
        print(f"[+]: {message}") 
        num_packets = int(message.split()[0])        # grabs "#" and converts to int

        for i in range(num_packets):
            rawPacket = self.client.recv(4096)
            print(f"Client: Raw packet received --> {rawPacket.decode()}")
            self.Receive_Packet(rawPacket)
            TCP_Server_Data.dataPending = False
            print()


    #Decode and parse a packet
    def Receive_Packet(self, data):
        # Step 1: Read the first 3 bytes to get the length
        length = int(data[:3].decode('ascii').lstrip('0') or '0')
    
        # Step 2: Read that many bytes of base64
        b64 = data[3:3 + length]
    
        # Step 3: Decode base64 back to raw bytes
        raw = base64.b64decode(b64)
    
        # Step 4: First byte is the Packet ID
        packet_id = raw[0]
    
        # Step 5: Parse remaining bytes as floats based on Packet ID
        if packet_id == 0:   # BME
            t, h, p, a = struct.unpack_from('<ffff', raw, offset=1)
            print(f"[BME] Temp={t:.2f}  Humidity={h:.2f}  Pressure={p:.2f}  Altitude={a:.2f}")
    
        elif packet_id == 1: # IMU
            ax, ay, az, gx, gy, gz = struct.unpack_from('<ffffff', raw, offset=1)
            print(f"[IMU] Accel=({ax:.2f},{ay:.2f},{az:.2f})  Gyro=({gx:.2f},{gy:.2f},{gz:.2f})")
    
        elif packet_id == 2: # GPS
            lat, lon = struct.unpack_from('<ff', raw, offset=1)
            print(f"[GPS] Lat={lat:.6f}  Lon={lon:.6f}")
    
        elif packet_id == 3: # MAG
            heading, = struct.unpack_from('<f', raw, offset=1)
            print(f"[MAG] Heading={heading:.2f}")








        