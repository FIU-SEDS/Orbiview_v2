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
        greenpen = pg.mkPen(color = (0, 255, 0), width = 10) #pen style variable

    

        #Reading data from flight logs CSV
        flightlogs = np.loadtxt("\\Users\\cbres\\OneDrive\\Documents\\ProgrammingProjects\\FIU_SEDS\\2025-2026_Dashboard\\Orbiview_v2\\Flight_Test_Data\\Flight_Data_2025-04-12_10-59-03 copy.csv", delimiter=",", skiprows=1)
        rows = np.arange(1, 21) #makes list of numbers from as (a, b) to include from a to b-1
        time_elapsed = flightlogs[0:20, 6]
        flightlogs[0:20, 6] = rows
        accel_y = flightlogs[0:20, 1]

        accel_x = flightlogs[0:20, 0]




        #Create the Legend
        legend = self.graphWidget.addLegend()
        legend.setBrush(pg.mkBrush(30, 30, 30, 200))       # background color (RGBA)
        legend.setPen(pg.mkPen(color='white', width=2))    # border color + thickness


        self.curve = self.graphWidget.plot(time_elapsed, accel_y, pen=redpen, name = "Accel_y", symbol = 'o', symbolsize = 20, symbolBrush = "black")
        self.Ycurve_visible = True #Tracks visibility

        self.Xcurve = self.graphWidget.plot(time_elapsed, accel_x, pen=greenpen, name = "Accel_x", symbol = 'o', symbolsize = 20, symbolBrush = "white")
        


        # === Toggle Button ===

        
        # self.Ycurve_visible = True #Tracks visibility
        # self.toggle_button = QtWidgets.QPushButton("Hide Line", self.graphWidget)
        # self.toggle_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #444;
        #         color: white;
        #         border: 1px solid #888;
        #         border-radius: 6px;
        #         padding: 5px 10px;
        #     }
        #     QPushButton:hover {
        #         background-color: #666;
        #     }
        # """)
        # self.toggle_button.move(1000, 20)  # Position top-right corner
        # self.toggle_button.setFixedSize(80, 25)
        # self.toggle_button.clicked.connect(self.toggle_curve)
        


        # === Toggle CheckBox ===
        self.check_toggle = QtWidgets.QCheckBox(self.graphWidget)
        self.check_toggle.setChecked(True)
        self.check_toggle.setStyleSheet("""
        QCheckBox {
            color: white;
            font-size: 12pt;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        """)
        self.check_toggle.move(self.graphWidget.width() - 580, 70) #These values align, but we need to find a better way for positioning
        #Qt creator should make positioning for checkbox easier
        #Also, when checkbox is selected, the red line goes lower on the legend and no longer aligns
        self.check_toggle.stateChanged.connect(self.toggle_curve)

    def toggle_curve(self, event):
        #Toggles the line's visibility when the line itself is clicked.
        if self.Ycurve_visible == True:
            self.graphWidget.removeItem(self.curve)
            self.check_toggle.setText("Show Line")
        else:
            self.graphWidget.addItem(self.curve)
            self.check_toggle.setText("Hide Line")
        self.Ycurve_visible = not self.Ycurve_visible



        
app = QtWidgets.QApplication(sys.argv)
windowicon = QtGui.QIcon('seds.png')
app.setWindowIcon(windowicon)
main = MainWindow()
main.show()
app.exec()