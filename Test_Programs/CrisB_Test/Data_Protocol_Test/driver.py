from PyQt6.QtWidgets import QApplication, QWidget
from TCP_Client_Data import TCP_Client_Data
from TCP_Server_Data import TCP_Server_Data
import threading
import time
import sys

class MainWindow(TCP_Server_Data, TCP_Client_Data, QWidget):
    def __init__(self):
        super().__init__()

        #TCP Server launches
        self.server_thread = threading.Thread(target = self.Server_Data_Setup, daemon = True) #daemon --> If main program exits, this thread is killed as well
        self.server_thread.start()
        time.sleep(1) #Wait 1 sec

        #TCP Client launches
        self.client_thread = threading.Thread(target = self.ClientDataSetup, daemon = True)
        self.client_thread.start()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()