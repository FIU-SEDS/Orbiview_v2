import sys

from PySide6 import QtWidgets 
from PySide6 import QtCore
import pyqtgraph as pg  
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.setFixedSize(1280,720)
        #Dimensions of 1280x720
        self.graphWidget.setBackground("black")
    

        #Reading data from flight logs CSV
        flightlogs = np.loadtxt("\\Users\\cbres\\OneDrive\\Documents\\ProgrammingProjects\\FIU_SEDS\\2025-2026_Dashboard\\Orbiview_v2\\Flight_Test_Data\\Flight_Data_2025-04-12_10-59-03 copy.csv", delimiter=",", skiprows=1)
        rows = np.arange(1, 21) #makes list of numbers from as (a, b) to include from a to b-1
        flightlogs[0:20, 6] = rows
        accel_y = flightlogs[0:20, 1]
        time_elapsed = flightlogs[0:20, 6]
        #print(accel_y)
        print(time_elapsed)

        
        self.curve = self.graphWidget.plot(time_elapsed, accel_y, pen={'color': 'r', 'width': 10})
        self.curve_visible = True #Tracks visibility




        


app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec()