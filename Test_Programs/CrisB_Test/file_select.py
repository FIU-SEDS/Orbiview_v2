from Oberview_v2_GUI_Design_redone import Ui_MainWindow
from PyQt6.QtWidgets import QFileDialog
from datetime import date
import os
import sys 

class Data_File():
    def ChooseFolderPath(self):

        parent_folder = QFileDialog.getExistingDirectory(
            self,                                                # parent window
            "Select parent directory for flightlogs folder",     # dialog title
            ""                                                   # Starting directory ("" = default)
        )

        if (parent_folder): #if valid directory exists
            print(parent_folder)
            #Builds directory for FlightLogs Folder
            self.flightlogs_folder_path = os.path.join(parent_folder, "FlightLogs_Folder")
            #Creates FlightLogs Folder
            os.makedirs(self.flightlogs_folder_path, exist_ok = True) #If folder already exist, program won't crash

            self.CreateFile()
        else:
            #Program closes
            print("No path selected. Exiting program...")
            #Will add UI notification later
            sys.exit()
    
    def CreateFile(self): #if no valid directory exists        
        file_directory = self.CreateFileDirectory() #includes file name

        with open(file_directory, "w") as csv_file:
            pass
        
    def CreateFileDirectory(self):
        today = date.today()
        today_launch_count = 0

        file_dir = ""
        new_file_pending = True
        pending_file_name = f"FlightLog_Data_{today}"

        while new_file_pending == True:
            if (today_launch_count < 1):
                if os.path.exists(f"{self.flightlogs_folder_path}/{pending_file_name}.csv"):
                    today_launch_count += 1
                else:
                    new_file_pending = False
                    file_dir = f"{self.flightlogs_folder_path}/{pending_file_name}.csv"
            else:
                if os.path.exists(f"{self.flightlogs_folder_path}/{pending_file_name}_Launch{today_launch_count}.csv"):
                    today_launch_count += 1
                else:
                    new_file_pending = False
                    file_dir = f"{self.flightlogs_folder_path}/{pending_file_name}_Launch{today_launch_count}.csv"

        return file_dir
        
        #Now will have to adjust the launch of some functions in main.py and PlotData accordingly
        #Might add file select button???