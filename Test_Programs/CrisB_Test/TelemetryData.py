from Oberview_v2_GUI_Design_redone import Ui_MainWindow
import PlotData
import numpy as np
import os
import pyqtgraph as pg
import PyQt6.QtCore as QtCore
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import QTimer

receiverOn = False
signalOn = False

class TelemetrySetup:
    def setupTelemetry(self): 
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        #Temporary --> Just for renaming purpose
        self.TelemetryTableWidget = self.tableWidget

        for row in range(self.TelemetryTableWidget.rowCount()):
            for col in range(self.TelemetryTableWidget.columnCount()):
                # Retrieve column name
                column_name = self.TelemetryTableWidget.horizontalHeaderItem(col).text().lower()

                # Get data based on column name
                value = self.searchData(column_name)  
                item = QTableWidgetItem(str(value))  
                self.TelemetryTableWidget.setItem(row, col, item)
                
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter) #Realigns item

        #No data inputted for altitude currently
    
    def searchData(self, column_name): #Will work on optimizing and fixing this function later
        #Searches for the correct column index based on the column name
        header = np.genfromtxt(PlotData.file_path, delimiter=",", max_rows=1, dtype=str)

        try:
            col_index = np.where(header == column_name)[0][0]
            return PlotData.flightlogs[-1, col_index]
        except IndexError:
            print(f"Column '{column_name}' not found in the CSV file.") #Debating on if this is necessary?
            return "N/A"
    
    def SetupTimers(self):
        #Sets up timers for updating telemetry data and receiver/signal status

        #Create a timer 
        self.timer = QTimer()

        # Concept for updating telemetry data periodically
        #self.timer.timeout.connect(self.updateTelemetryData)
        #self.timer.start(1000)  # Update every second

        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.ReceiverAndSignalStatus)
        self.status_timer.start(1000)  # Update every second

    def ReceiverAndSignalStatus(self): #How exactly is this meant to work???
        #rssi_value = self.searchData("rssi")
        #signal_to_noise_value = self.searchData("signal to noise")

        #self.RSSIValueLabel.setText(str(rssi_value) + " dBm")
        #self.SignalToNoiseValueLabel.setText(str(signal_to_noise_value) + " dB")

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

        