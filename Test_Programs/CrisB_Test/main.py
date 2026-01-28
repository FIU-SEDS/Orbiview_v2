from Orbiview_V1 import PortSelectionDialog  # Just import it
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


class MainWindow(Ui_MainWindow, ButtonFunctions, PlotData, TelemetrySetup, Data_File, TCP_Server_Setup, TCPClient, QWidget):
    def __init__(self):
        super().__init__()

        dialog = PortSelectionDialog(self)
        if dialog.exec():
            port = dialog.get_selected_port()
            baudrate = dialog.get_selected_baudrate()
            print(f"Selected: {port} at {baudrate} baud")

        #File path is selected
        self.ChooseFolderPath()

        #TCP Server launches
        self.server_thread = threading.Thread(target = self.Server_Startup, daemon = True) #daemon --> If main program exits, this thread is killed as well
        self.server_thread.start()
        time.sleep(2) #Wait 1 sec

        #TCP Client launches
        self.client_thread = threading.Thread(target = self.Client_Setup, daemon = True)
        self.client_thread.start()

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