from Oberview_v2_GUI_Design_redone import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QWidget
import sys
import numpy as np
import pyqtgraph as pg
import os

#get the folder where flight data is
script_dir = os.path.dirname(os.path.abspath(__file__))

#Reading data from flight logs CSV
file_path = os.path.join(script_dir, "..", "..", "Flight_Test_Data", "Flight_Data_2025-04-12_10-59-03 copy.csv")
file_path = os.path.abspath(file_path)  # Make CSV file path absolute
flightlogs = np.loadtxt(file_path, delimiter=",", skiprows=1)

#Re-arrange data for plotting
rows = np.arange(1, 21)
flightlogs[0:20, 6] = rows
time_elapsed = flightlogs[0:20, 6]

#Define flightlogs data
x_velocity = flightlogs[0:20, 0]
y_velocity = flightlogs[0:20, 1]
z_velocity = flightlogs[0:20, 2]


class MainWindow(QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        #Window resize - could work some functionality later?
        self.gridLayoutWidget.resize(1280, 720)
        self.resize(1280, 720)

        self.plot()

    def plot(self):
        x_velocity_curve = self.Graph1.plot(time_elapsed, x_velocity, pen=pg.mkPen(color=(255, 0, 0), width=2), name="X Velocity")
    
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()