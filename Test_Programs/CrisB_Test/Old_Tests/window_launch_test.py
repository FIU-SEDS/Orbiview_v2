from file_select import Data_File
from PyQt6.QtWidgets import QApplication, QWidget
import sys

class MainWindow(Data_File, QWidget):
    def __init__(self):
        super().__init__()
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()