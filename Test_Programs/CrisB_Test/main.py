from Oberview_v2_GUI_Design_redone import Ui_MainWindow
from ButtonFunctionality import ButtonFunctions
from PlotData import PlotData
from TelemetryData import TelemetrySetup
from PyQt6.QtWidgets import QApplication, QWidget
import sys

class MainWindow(Ui_MainWindow, ButtonFunctions, PlotData, TelemetrySetup, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupButtons()

        #Window resize - could work some functionality later?
        #These currently aren't necessary because mainwindow and centralwidget are already set to 1280x720 in the GUI design
        #self.gridLayoutWidget.resize(1280, 720) 
        #self.resize(1280, 720)

        self.Initialplot()
        self.buttonClick()
        self.checkbox_functionality()
        self.SetupTimers()
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()