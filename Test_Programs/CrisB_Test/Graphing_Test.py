#Will test PyQt6 Graphs here
import sys

from PySide6 import QtWidgets 
from PySide6 import QtCore
import pyqtgraph as pg  # import PyQtGraph after Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)


        # plot data: x, y values
        hour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [0, 30, 32, 34, 32, 33, 31, 29, 32, 35, 45,]

        hour2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature2 = [0, 13, 11, 18, 22, 18, 17, 23, 29, 51, 49]
        
        
        
        self.setFixedSize(1280,720)
        #Dimensions of 1280x720
        self.graphWidget.setBackground("black")
        
 
        self.curve = self.graphWidget.plot(hour, temperature, pen={'color': 'r', 'width': 10})
        self.curve_visible = True #Tracks visibility

        self.greencurve = self.graphWidget.plot(hour2, temperature2, pen={'color': 'g', 'width': 10, 'style': QtCore.Qt.DashLine})


        # === Toggle Button ===
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
main = MainWindow()
main.show()
app.exec()