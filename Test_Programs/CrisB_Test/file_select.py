from Oberview_v2_GUI_Design_redone import Ui_MainWindow
from PyQt6.QtWidgets import QFileDialog

class Data_File():
    def ChooseFilePath(self):
        file_path, _ = QFileDialog.getOpenFileName(
        self,                       # parent window
        "Select a file",            # dialog title
        "",                         # starting directory ("" = default)
        "CSV Files (*.csv);;All Files (*)"
)
        
        #Now will have to adjust the launch of some functions in main.py and PlotData accordingly
        #Might add file select button???