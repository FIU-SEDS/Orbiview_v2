import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
import pyqtgraph as pg 
# from layout_colorwidget import Color
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Acceleration Y over Time Elapsed")

        self.graph = pg.PlotWidget()

        file = pd.read_csv('\\Users\\cmdia\\Desktop\\leethax0r\\seds\\Orbiview_v2\\Test_Programs\\CarlosD_Test\\DATALOG.csv')

        accel_y = file['AccelY'].tolist()
        time_ms = file['Milliseconds'].tolist()

        self.graph.plot(time_ms, accel_y)

        self.graph.setLabel("left", "Time (ms)", )
        self.graph.setLabel("bottom", "Acceleration Y ", )
        self.graph.addLegend()

















        
        self.setCentralWidget(self.graph)

        


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()