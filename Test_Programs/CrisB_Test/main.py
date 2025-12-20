from Oberview_v2_GUI_Design_redone import Ui_MainWindow
from ButtonFunctionality import ButtonFunctions
from PlotData import PlotData
from TelemetryData import TelemetrySetup
from PyQt6.QtWidgets import QApplication, QWidget
from file_select import Data_File
import sys

class MainWindow(Ui_MainWindow, ButtonFunctions, PlotData, TelemetrySetup, Data_File, QWidget):
    def __init__(self):
        super().__init__()
        #File path is selected
        self.ChooseFolderPath()

        #Program UI launches
        self.setupUi(self)

        #Button Functionality is implemented with UI
        self.setupButtons()
        self.buttonClick()
        self.checkbox_functionality()

        #Window resize - could work some functionality later?
        #These currently aren't necessary because mainwindow and centralwidget are already set to 1280x720 in the GUI design
        #self.gridLayoutWidget.resize(1280, 720) 
        #self.resize(1280, 720)

        #Initial data and graphs are implemented, then program starts checking for new data
        self.Initialplot()
        self.SetupTimers()
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()