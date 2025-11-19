from Oberview_v2_GUI_Design_redone import Ui_MainWindow
from ButtonFunctionality import ButtonFunctions
from PyQt6.QtWidgets import QApplication, QWidget
import sys
import numpy as np
import pyqtgraph as pg
import os
import time


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


class MainWindow(Ui_MainWindow, ButtonFunctions, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.zoomed_in = False  # Initial zoom state

        #Window resize - could work some functionality later?
        self.gridLayoutWidget.resize(1280, 720)
        self.resize(1280, 720)

        self.plot()
        self.buttonClick()

    def filterCurvies(self):
        pass

    def plot(self):
        #Couple of suggestion: Graph titles, Axes titles (and units), grid lines
        #When UI file is done, implement these suggestions in UI file

        #Graph 1 - Directional velocities
        x_velocity_curve = self.Graph1.plot(time_elapsed, x_velocity, pen=pg.mkPen(color=(255, 0, 0), width=2), name="X Velocity")
        y_velocity_curve = self.Graph1.plot(time_elapsed, y_velocity, pen=pg.mkPen(color=(0, 255, 0), width=2), name="Y Velocity")
        z_velocity_curve = self.Graph1.plot(time_elapsed, z_velocity, pen=pg.mkPen(color=(0, 0, 255), width=2), name="Z Velocity")

        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()