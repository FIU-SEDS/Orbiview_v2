from Oberview_v2_GUI_Design_redone import Ui_MainWindow
import numpy as np
import os
import pyqtgraph as pg

#get the folder where flight data is
script_dir = os.path.dirname(os.path.abspath(__file__))

#Reading data from flight logs CSV
file_path = os.path.join(script_dir, "..", "..", "Flight_Test_Data", "Flight_Data_2025-04-12_10-59-03 copy.csv")
file_path = os.path.abspath(file_path)  # Make CSV file path absolute
flightlogs = np.loadtxt(file_path, delimiter=",", skiprows=1)

#Re-arrange data for plotting
rows = np.arange(1, 21)
flightlogs[0:20, 6] = rows
time_elapsed = flightlogs[0:20, 6]

#Define flightlogs data
x_velocity = flightlogs[0:20, 0]
y_velocity = flightlogs[0:20, 1]
z_velocity = flightlogs[0:20, 2]

#placeholder --> Will get data from different/new file
altitude = flightlogs[0:20, 4]

rssi_data = flightlogs[0:20, 8]

class PlotData:
    def plot(self):

        #Graph 1 - Acceleration
        self.x_velocity_curve = self.Graph1.plot(time_elapsed, x_velocity, pen=pg.mkPen(color=(255, 0, 0, 255), width=2), name="X Velocity")
        self.y_velocity_curve = self.Graph1.plot(time_elapsed, y_velocity, pen=pg.mkPen(color=(0, 255, 0, 255), width=2), name="Y Velocity")
        self.z_velocity_curve = self.Graph1.plot(time_elapsed, z_velocity, pen=pg.mkPen(color=(0, 0, 255, 255), width=2), name="Z Velocity")
        self.Graph1.setTitle("Acceleration")
        self.Graph1.setLabel('left', 'Velocity', 'm/s') #Check units later

        #Graph 2 - Altitude
        self.altitude_curve = self.Graph2.plot(time_elapsed, altitude, pen=pg.mkPen(color=(255, 0, 0, 255), width=2), name="Altitude")    
        self.Graph2.setTitle("Altitude")
        self.Graph2.setLabel('left', 'Altitude', 'ft') 

        #Graph 3 - RSSI
        self.RSSI_curve = self.Graph3.plot(time_elapsed, rssi_data, pen=pg.mkPen(color=(255, 0, 0, 255), width=2), name="RSSI")
        self.Graph3.setTitle("RSSI")
        self.Graph3.setLabel('left', 'RSSI', 'dBm') 

        for graph in [self.Graph1, self.Graph2, self.Graph3]:
            graph.showGrid(x=True, y=True)
            graph.setLabel('bottom', 'Time Elapsed', 's')

        
    def SearchCurves(self, selectedCheckbox):
        #Make sure to add new checkboxes and curves here if more are added
        self.checkbox_dictionary = {
            self.CurveXCheckBox: self.x_velocity_curve,
            self.CurveYCheckBox: self.y_velocity_curve,
            self.CurveZCheckBox: self.z_velocity_curve,
            self.AltitudeCheckBox: self.altitude_curve,
            self.RSSICheckBox: self.RSSI_curve
        }

        return(self.checkbox_dictionary[selectedCheckbox])
    
    #New goal: update data with built in timer
    #Comment: might need to add new add or change data file (and their paths) later on
        #Thus might need to change column indexes

        


