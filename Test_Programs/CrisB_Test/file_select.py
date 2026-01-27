from PyQt6.QtWidgets import QFileDialog
from datetime import date
import os
import sys
import csv

class Data_File():
    def ChooseFolderPath(self):
        parent_folder = QFileDialog.getExistingDirectory(
            self,                                                # parent window
            "Select parent directory for flightlogs folder (new or existing)",     # dialog title
            ""                                                   # Starting directory ("" = default)
        )

        if (parent_folder): #if valid directory exists
            print(parent_folder)
            #Builds directory for FlightLogs Folder
            self.flightlogs_folder_path = os.path.join(parent_folder, "FlightLogs_Folder")
            #Creates FlightLogs Folder
            os.makedirs(self.flightlogs_folder_path, exist_ok = True) #If folder already exist, program won't crash and continues as normal

            self.CreateFile()
        else: #if no valid directory exists
            #Program closes
            print("No path selected. Exiting dashboard program...")
            #Will add UI notification later
            sys.exit()
    
    def CreateFile(self):         
        self.data_file_directory = self.CreateFileDirectory() #includes file name

        #Create csv file
        with open(self.data_file_directory, "w", newline="") as data_file: #'w' --> write mode creates the file
            self.writer = csv.writer(data_file) #Creates writer object
            self.headers = ["acceleration x", "acceleration y", "acceleration z", "altitude", "rssi", "time_elapsed"]

            self.writer.writerow(self.headers)

        #Will work on this function as next step --> Maybe set up columns with headers?
        
    def CreateFileDirectory(self):
        today = date.today()
        today_launch_count = 0

        file_dir = ""
        new_file_pending = True
        pending_file_name = f"FlightLog_Data_{today}"

        while new_file_pending == True:
            if (today_launch_count < 1):
                #if os.path.exists(f"{self.flightlogs_folder_path}/{pending_file_name}.csv"):
                if os.path.exists(os.path.join(self.flightlogs_folder_path, f"{pending_file_name}.csv")):
                    today_launch_count += 1
                else:
                    new_file_pending = False
                    #file_dir = f"{self.flightlogs_folder_path}/{pending_file_name}.csv"
                    file_dir = os.path.join(self.flightlogs_folder_path, f"{pending_file_name}.csv")
            else: #if today_launch_count >= 1
                #if os.path.exists(f"{self.flightlogs_folder_path}/{pending_file_name}_Launch{today_launch_count}.csv"):
                if os.path.exists(os.path.join(self.flightlogs_folder_path, f"{pending_file_name}_Launch{today_launch_count}.csv")):
                    today_launch_count += 1
                else:
                    new_file_pending = False
                    #file_dir = f"{self.flightlogs_folder_path}/{pending_file_name}_Launch{today_launch_count}.csv"
                    file_dir = os.path.join(self.flightlogs_folder_path, f"{pending_file_name}_Launch{today_launch_count}.csv")

        return file_dir
        
        #Utilized os.path.join to prevent potential file errors in Linux and Mac OS

        #Now will have to adjust the launch of some functions in main.py and PlotData accordingly
        #Might add file select button???