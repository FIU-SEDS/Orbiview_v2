from Orbiview_V1 import PortSelectionDialog  
from serial_reader import SerialReader  
from Oberview_v2_GUI_Design_redone import Ui_MainWindow
from ButtonFunctionality import ButtonFunctions
from PlotData import PlotData
from TelemetryData import TelemetrySetup
from file_select import Data_File
from TCP_Server import TCP_Server_Setup
from TCP_Client import TCPClient
from PyQt6.QtWidgets import QApplication, QWidget
import sys
import threading
import time


class MainWindow(Ui_MainWindow, ButtonFunctions, PlotData, TelemetrySetup, Data_File, TCP_Server_Setup, TCPClient, SerialReader, QWidget):
    def __init__(self):
        super().__init__()
        
        #Create data values
        self.accel_x_data = []
        self.accel_y_data = []
        self.accel_z_data = []
        self.altitude_data = []
        self.rssi_data = []
        self.time_data = []
        self.receiver_history = []
        self.signal_history = []
        self.data_arrays = [self.accel_x_data, self.accel_y_data, self.accel_z_data, self.altitude_data, self.rssi_data, self.time_data, self.receiver_history, self.signal_history]

        #Oberview_V1 starting program launches - User selects baudrate and serial port
        dialog = PortSelectionDialog(self)
        if dialog.exec():
            self.port = dialog.get_selected_port()
            self.baudrate = dialog.get_selected_baudrate()

        #File path is selected
        self.ChooseFolderPath()

        #Only use placeholder data if no baudrate and serial port are selected

        #TCP Server launches
        self.server_thread = threading.Thread(target = self.Server_Startup, daemon = True) #daemon --> If main program exits, this thread is killed as well
        self.server_thread.start()
        time.sleep(2) #Wait 1 sec

        #TCP Client launches
        self.client_thread = threading.Thread(target = self.Client_Setup, daemon = True)
        self.client_thread.start()

        #Create thread for serial reader
        self.serial_thread = threading.Thread(target = self.simple_serial_reader, args = (self.port, self.baudrate), daemon = True)
        self.serial_thread.start()

        #Program UI launches
        self.setupUi(self)

        #Button Functionality is implemented with UI
        self.setupButtons()
        self.buttonClick()
        self.checkbox_functionality()

        #Window resize - could work some functionality later?
        #These currently aren't necessary because mainwindow and centralwidget are already set to 1280x720 in the GUI design
        #self.gridLayoutWidget.resize(1280, 720) 
        #self.resize(1280, 720)

        #Initial data and graphs are implemented, then program starts checking for new data
        self.Initialplot()
        self.SetupTelemtryTimers()
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()