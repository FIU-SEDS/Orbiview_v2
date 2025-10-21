#Will test PyQt6 Graphs here
import sys

from PySide6 import QtWidgets
import pyqtgraph as pg  # import PyQtGraph after Qt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45,]
        # plot data: x, y values
        
        
        self.setFixedSize(1280,720)
        #Dimensions of 1280x720
        self.graphWidget.setBackground("black")
        
 
        self.graphWidget.plot(hour, temperature, pen = "r")
        #pen = r sets red color


app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec()