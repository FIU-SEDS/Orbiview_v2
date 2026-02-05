import serial
import time

class SerialReader():
    def simple_serial_reader(self, port, baudrate): #default values?
        """
        Simple function that:
        1. Connects to serial port
        2. Waits for data
        3. Returns parsed data when it arrives
        """
            
        # Step 2: CONNECT
        try:
            ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
            print(f"\nSelected: {port} at {baudrate} baud\n")
            time.sleep(2)  # Let connection stabilize
        except Exception as e:
            print(f"Failed to connect: {e}")
            return None
        
        previous_message = ""

        # Step 3 & 4: WAIT and READ
        while True:
            try:
                if ser.in_waiting:  # Data available? --> Requires transmitter & receiver
                    print("Listening for data")
                    line = ser.readline().decode('utf-8').strip()
                    
                    if "+RCV=" in line:
                        # Parse it
                        clean_data = line.replace("+RCV=", "")
                        values = clean_data.split(',')
                        
                        if len(values) >= 8: #Protects against corrupted / incomplete serial data
                            parsed_data = {
                                'sensor_data': {
                                    'accel_x': float(values[0]),
                                    'accel_y': float(values[1]),
                                    'accel_z': float(values[2]),
                                    'altitude': float(values[3]),
                                    'rssi': float(values[4]),
                                    'time': int(values[5])
                                },
                                'status': {
                                    'receiver': values[6],  # "ON" or "OFF"
                                    'signal': values[7]     # "ON" or "OFF"
                                }
                            }
                            
                            self.handle_serial_data(parsed_data)
                else:
                    #To only print error message once
                    error_string = "---No receiver and/or transmitter---" 
                    if (previous_message != error_string):
                        print(error_string)
                        previous_message = error_string

                time.sleep(0.05)  # Small delay
                
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(0.5)

    #Confirms data is picked up
    def handle_serial_data(self, data):
        """Called automatically every time serial data arrives"""

        print(f"new data set arrived: {data}")
        sensor = data['sensor_data']
        status = data['status']


        if data == None: #Ensures no connection failure --> Maybe attempt to reconnect?
            print("Warning: received no data!")
            return #exit function early


        print(f"\nReceived new data set: {data}\n")

        self.accel_x_data.append(sensor['accel_x'])
        self.accel_y_data.append(sensor['accel_y'])
        self.accel_z_data.append(sensor['accel_z'])
        self.altitude_data.append(sensor['altitude'])
        self.rssi_data.append(sensor['rssi'])
        self.time_data.append(sensor['time'])

        self.receiver_history.append(status['receiver'])
        self.signal_history.append(status['signal'])