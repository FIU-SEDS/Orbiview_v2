from Oberview_v2_GUI_Design_redone import Ui_MainWindow
import PlotData
import numpy as np
import PyQt6.QtCore as QtCore
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import QTimer

receiverOn = False
signalOn = False
previous_error_message = ""

class TelemetrySetup:
    def SetupTimers(self):
        #Sets up timers for updating telemetry data and receiver/signal status

        #Create a timer 
        self.telemetrytimer = QTimer()
        self.telemetrytimer.timeout.connect(self.ReceiverAndSignalStatus)
        self.telemetrytimer.timeout.connect(self.setupTelemetry)
        self.telemetrytimer.start(1000)  # Update every second
    
    def setupTelemetry(self): 
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        #Temporary --> Just for renaming purpose
        self.TelemetryTableWidget = self.tableWidget

        for row in range(self.TelemetryTableWidget.rowCount()):
            for col in range(self.TelemetryTableWidget.columnCount()):
                # Retrieve column name
                column_name = self.TelemetryTableWidget.horizontalHeaderItem(col).text().lower()

                # Get data based on column name
                value = self.searchforTelemetryData(column_name)  
                item = QTableWidgetItem(str(value))  
                self.TelemetryTableWidget.setItem(row, col, item)
                
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter) #Realigns item

        #No data inputted for altitude currently

    def searchforTelemetryData(self, column_name): #Will work on optimizing and fixing this function later
        #Searches for the correct column index based on the column name
        header = np.genfromtxt(PlotData.file_path, delimiter=",", max_rows=1, dtype=str)
        
        global previous_error_message

        try:
            col_index = np.where(header == column_name)[0][0]
            return PlotData.flightlogs[-1, col_index]
        except IndexError:
            error_message = f"Column '{column_name}' not found in the CSV file."
            if previous_error_message != error_message:
                print(error_message) #Will only print if different from last error
            previous_error_message = error_message
            return "N/A"

    def ReceiverAndSignalStatus(self): #How exactly is this meant to work???
        #Need to ask how exactly we're going to measure RSSI, Signal Status, and Receiver Status
        if receiverOn == True:
            self.ReceiverColorIcon.setStyleSheet("background-color: rgb(0, 255, 0);\n" "border-radius: 10px;")
            #self.ReceiverStatusLabel.setText("ON")
        else:
            self.ReceiverColorIcon.setStyleSheet("background-color: rgb(255, 0, 0);\n" "border-radius: 10px;")
            #self.ReceiverStatusLabel.setText("OFF")

        if signalOn == True:
            self.SignalColorIcon.setStyleSheet("background-color: rgb(0, 255, 0);\n" "border-radius: 10px;")
            #self.SignalStatusLabel.setText("ON")
        else:
            self.SignalColorIcon.setStyleSheet("background-color: rgb(255, 0, 0);\n" "border-radius: 10px;")
            #self.SignalStatusLabel.setText("OFF")

        