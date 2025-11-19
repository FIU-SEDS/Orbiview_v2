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
        
        self.zoomed_in = False

        #Window resize - could work some functionality later?
        self.gridLayoutWidget.resize(1280, 720)
        self.resize(1280, 720)

        self.plot()
        self.ZoomResize()

    def plot(self):
        x_velocity_curve = self.Graph1.plot(time_elapsed, x_velocity, pen=pg.mkPen(color=(255, 0, 0), width=2), name="X Velocity")

    def ZoomResize(self):
        self.ZoomButton1.clicked.connect(lambda: self.Zoom_Change(self.ZoomButton1, self.Graph1))
        self.ZoomButton3.clicked.connect(lambda: self.Zoom_Change(self.ZoomButton3, self.Graph2)) #Wrong button placed
        self.ZoomButton2.clicked.connect(lambda: self.Zoom_Change(self.ZoomButton2, self.Graph3)) #Wrong button placed
        self.ZoomButton4.clicked.connect(lambda: self.Zoom_Change(self.ZoomButton4, self.Graph4))
    
    def Zoom_Change(self, selectedButton, selectedGraph):
        keep_widgets = {selectedButton, selectedGraph, self.centralwidget, self.gridLayoutWidget}

        if self.zoomed_in == False:
            # Iterate over all child widgets in the window
            for widgets in self.findChildren(QWidget):
                if widgets not in keep_widgets and widgets not in selectedGraph.findChildren(QWidget):
                    widgets.setVisible(False)
            selectedButton.setText("Zoom Out")

        if self.zoomed_in == True:
            for widgets in self.findChildren(QWidget):
                widgets.setVisible(True)
            selectedButton.setText("Zoom In")

        self. zoomed_in = not self.zoomed_in


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()