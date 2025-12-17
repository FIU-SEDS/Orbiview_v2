from Oberview_v2_GUI_Design_redone import Ui_MainWindow
from PlotData import PlotData
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget
from pyqtgraph import PlotWidget
import pyqtgraph as pg

class ButtonFunctions(PlotData):


    def setupButtons(self):
        #Temporary --> Just for renaming purpose
        self.AltitudeCheckBox = self.checkBox_7
        self.RSSICheckBox = self.checkBox_8

        #Set all check boxes to false
        self.checkboxes = [checkbox for checkbox in self.findChildren(QtWidgets.QCheckBox)]
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

    def buttonClick(self):
        #triggers for zoom_change function
        self.ZoomButton1.clicked.connect(lambda: self.zoom_change(self.ZoomButton1, self.Graph1))
        self.ZoomButton2.clicked.connect(lambda: self.zoom_change(self.ZoomButton2, self.Graph2)) 
        self.ZoomButton3.clicked.connect(lambda: self.zoom_change(self.ZoomButton3, self.Graph3)) 

        #triggers for button color change function
        for button in [self.ZoomButton1, self.ZoomButton2, self.ZoomButton3]:
            button.pressed.connect(lambda b=button: b.setStyleSheet("color: rgb(0, 0, 0);\n" "background-color: rgb(153, 204, 255);\n"))
            button.released.connect(lambda b=button: b.setStyleSheet("color: rgb(0, 0, 0);\n" "background-color: rgb(255, 255, 255);\n"))
    
    def zoom_change(self, selectedButton, selectedGraph):
        keep_widgets = {selectedButton, selectedGraph, self.centralwidget, self.gridLayoutWidget}

        if self.zoomed_in == False:
            # Iterate over all child widgets in the window
            for widgets in self.findChildren(QWidget):
                if widgets not in keep_widgets and widgets not in selectedGraph.findChildren(QWidget):
                    widgets.setVisible(False)
            selectedButton.setText("Zoom Out")

        if self.zoomed_in == True:
            for widgets in self.findChildren(QWidget):
                widgets.setVisible(True)
            selectedButton.setText("Zoom In")

        self.zoomed_in = not self.zoomed_in
    
    def checkbox_functionality(self):
        for checkbox in self.checkboxes:
            checkbox.stateChanged.connect(lambda state, cb=checkbox: self.filterCurves(cb, state))

    def filterCurves(self, selectedCheckbox, state):
        corr_curve = self.SearchCurves(selectedCheckbox)
        print(self.checkbox_dictionary[selectedCheckbox]) #Can remove later
        current_pen = corr_curve.opts['pen'] # Store the initial pen
        
        if state == QtCore.Qt.CheckState.Unchecked.value:
            new_pen = pg.mkPen(color=(current_pen.color().red(), current_pen.color().green(), current_pen.color().blue(), 0), width = 2)
            corr_curve.setPen(new_pen)

        else: #Checked
            new_pen = pg.mkPen(color=(current_pen.color().red(), current_pen.color().green(), current_pen.color().blue(), 255), width = 2)
            corr_curve.setPen(new_pen)
        
        

            





        




