from Oberview_v2_GUI_Design_redone import Ui_MainWindow
import numpy as np
import os
import pyqtgraph as pg
from PyQt6.QtCore import QTimer
import math

#get the folder where flight data is
script_dir = os.path.dirname(os.path.abspath(__file__))

#Reading data from flight logs CSV
file_path = os.path.join(script_dir, "..", "..", "Flight_Test_Data", "Flight_Data_2025-04-12_10-59-03 copy.csv") #WILL HAVE TO MODIFY WHEN ALTERING FILES
file_path = os.path.abspath(file_path)  # Make CSV file path absolute
flightlogs = np.loadtxt(file_path, delimiter=",", skiprows=1)

#Re-arrange data for plotting
number_of_rows = flightlogs.shape[0]
rows = np.arange(1, number_of_rows + 1)
flightlogs[:, 6] = rows
time_elapsed = flightlogs[:, 6]

#Define flightlogs data
x_velocity = flightlogs[:, 0]
y_velocity = flightlogs[:, 1]
z_velocity = flightlogs[:, 2]

#placeholder --> Will get data from different/new file
altitude = flightlogs[:, 4]

rssi_data = flightlogs[:, 8]

class PlotData:
    def Initialplot(self):
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

        self.TimingUpdate()
        
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
    
    def TimingUpdate(self):
        #Sets up timer for updating plots
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.UpdatePlots)
        self.plot_timer.start(1000)  # Update every second

    def UpdatePlots(self):
#       #How can i optimize this function?
        #Re-read data from flight logs CSV
        global flightlogs
        flightlogs = np.loadtxt(file_path, delimiter=",", skiprows=1)

        #Re-arrange data for plotting
        number_of_rows = flightlogs.shape[0]
        rows = np.arange(1, number_of_rows + 1)
        flightlogs[:, 6] = rows
        time_elapsed = flightlogs[:, 6]

        #Re-arrange data for plotting
        x_velocity = flightlogs[:, 0]
        y_velocity = flightlogs[:, 1]
        z_velocity = flightlogs[:, 2]
        altitude = flightlogs[:, 4]
        rssi_data = flightlogs[:, 8]

        #Updates plots based on current data
        self.x_velocity_curve.setData(time_elapsed, x_velocity)
        self.y_velocity_curve.setData(time_elapsed, y_velocity)
        self.z_velocity_curve.setData(time_elapsed, z_velocity)
        self.altitude_curve.setData(time_elapsed, altitude)
        self.RSSI_curve.setData(time_elapsed, rssi_data)

        self.UpdateTicks()

    def UpdateTicks(self):
        #Help determine max and min of graph to help create ticks
        for graph in [self.Graph1, self.Graph2, self.Graph3]:
            curves_in_graph = graph.listDataItems()
            cross_zero_count = 0

            if curves_in_graph == None: ##Can I remove this???
                continue

            global_min = float("inf")
            global_max = float("-inf")

            for curve in curves_in_graph:
                x,y = curve.getData() #Just focus on y h
                
                if y is None or len(y) == 0: #Ensures there are values for y
                    continue

                crosses_zero = (y.min() <= 0 and y.max() >= 0)
                if crosses_zero == True:
                    cross_zero_count += 1
                crosses_zero = False

                curve_min = y.min()
                curve_max = y.max()

                global_min = min(global_min, curve_min)
                global_max = max(global_max, curve_max)
            
            axis = graph.getAxis('left')

            if cross_zero_count > 0:
                major_ticks = {(global_min, f"{math.floor(global_min)}"), (0, "0"), (global_max, f"{math.ceil(global_max)}")}
                minor_ticks = {(round(global_min/2), f"{round(global_min/2)}"), (round(global_max/2), f"{round(global_max/2)}")}
            else:
                midpoint = (global_max + global_min)/2
                major_ticks = {(global_min, f"{math.floor(global_min)}"), (midpoint, f"{midpoint}"), (global_max, f"{math.ceil(global_max)}")}
                minor_ticks = {((global_min + midpoint)/2, f"{(global_min + midpoint)/2}"), ((global_max + midpoint)/2, f"{(global_max + midpoint)/2}")}
            axis.setTicks([major_ticks, minor_ticks])

    #Might need to add more rows for time elapsed as new data entries are added
    
    #New goal: update data with built in timer
    #Comment: might need to add new add or change data file (and their paths) later on
        #Thus might need to change column indexes