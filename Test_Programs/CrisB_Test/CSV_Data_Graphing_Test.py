import sys

from PySide6 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg  
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Acceleration Graph")
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        #Graph styling
        self.graphWidget.setTitle("Acceleration Forces Graph", size = "25pt", color = "w")
        self.setFixedSize(1280,720) #Dimensions of 1280x720
        self.graphWidget.setBackground("black")

        styles = {'color':'white','font-size':'20pt'} #not working when implemented???
        self.graphWidget.setLabel('left','Acceleration (mGal)')
        self.graphWidget.setLabel('bottom', 'Time (seconds)')

        redpen = pg.mkPen(color = (255,0,0), width = 10) #pen style variable
    

        #Reading data from flight logs CSV
        flightlogs = np.loadtxt("\\Users\\cbres\\OneDrive\\Documents\\ProgrammingProjects\\FIU_SEDS\\2025-2026_Dashboard\\Orbiview_v2\\Flight_Test_Data\\Flight_Data_2025-04-12_10-59-03 copy.csv", delimiter=",", skiprows=1)
        rows = np.arange(1, 21) #makes list of numbers from as (a, b) to include from a to b-1
        flightlogs[0:20, 6] = rows
        accel_y = flightlogs[0:20, 1]
        time_elapsed = flightlogs[0:20, 6]

        #print(accel_y)
        #print(time_elapsed)

        
        self.curve = self.graphWidget.plot(time_elapsed, accel_y, pen=redpen, symbol = 'o', symbolsize = 20, symbolBrush = "black")
        self.curve_visible = True #Tracks visibility


        # === Toggle Button ===
        self.curve_visible = True #Tracks visibility
        self.toggle_button = QtWidgets.QPushButton("Hide Line", self.graphWidget)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: 1px solid #888;
                border-radius: 6px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        self.toggle_button.move(1000, 20)  # Position top-right corner
        self.toggle_button.setFixedSize(80, 25)
        self.toggle_button.clicked.connect(self.toggle_curve)

    def toggle_curve(self, event):
        #Toggles the line's visibility when the line itself is clicked.
        if self.curve_visible == True:
            self.graphWidget.removeItem(self.curve)
            self.toggle_button.setText("Show Line")
        else:
            self.graphWidget.addItem(self.curve)
            self.toggle_button.setText("Hide Line")
        self.curve_visible = not self.curve_visible


        
app = QtWidgets.QApplication(sys.argv)
windowicon = QtGui.QIcon('seds.png')
app.setWindowIcon(windowicon)
main = MainWindow()
main.show()
app.exec()