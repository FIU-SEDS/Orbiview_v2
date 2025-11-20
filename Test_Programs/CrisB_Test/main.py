from Oberview_v2_GUI_Design_redone import Ui_MainWindow
from ButtonFunctionality import ButtonFunctions
from PlotData import PlotData
from PyQt6.QtWidgets import QApplication, QWidget
import sys

class MainWindow(Ui_MainWindow, ButtonFunctions, PlotData, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupButtons()

        self.zoomed_in = False  # Initial zoom state

        #Window resize - could work some functionality later?
        self.gridLayoutWidget.resize(1280, 720)
        self.resize(1280, 720)

        self.plot()
        self.buttonClick()
        self.checkbox_functionality()
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()