import serial
import time

def simple_serial_reader(port="COM3", baudrate=115200): #default values listed
    """
    Simple function that:
    1. Connects to serial port
    2. Waits for data
    3. Returns parsed data when it arrives
    """
    
    # Step 2: CONNECT
    try:
        ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        print(f"Connected to {port}")
        time.sleep(2)  # Let connection stabilize
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None
    
    # Step 3 & 4: WAIT and READ
    while True:
        try:
            if ser.in_waiting:  # Data available?
                line = ser.readline().decode('utf-8').strip()
                
                if "+RCV=" in line:
                    # Parse it
                    clean_data = line.replace("+RCV=", "")
                    values = clean_data.split(',')
                    
                    if len(values) >= 8:
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
                        
                        return parsed_data  # Return it to YOUR code
            
            time.sleep(0.05)  # Small delay
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(0.5)