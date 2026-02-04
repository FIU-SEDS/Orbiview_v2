import sys
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QDialogButtonBox)
from PyQt6.QtGui import QFont
from serial.tools import list_ports #Not sure why there is a warning?

#This script reconstructs the Obirview V1 launch program + UI to initiate the Obirview V2 program
#Upon launch user is to select serial port and baud rate

class PortSelectionDialog(QDialog):
    """Dialog for selecting a serial port"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Serial Port")
        self.resize(400, 200)
        
        # Set dark theme
        self.setStyleSheet("""
            QDialog, QWidget {
                background-color: #0D0D0D;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
                font-weight: bold;
            }
            QComboBox {
                background-color: #222222;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 5px;
                min-height: 25px;
            }
            QPushButton {
                background-color: #FFFFFF;
                color: #0D0D0D;
                border: none;
                padding: 8px 16px;
                min-height: 30px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Port selection
        self.label = QLabel("Receiver Serial Port:")
        self.label.setFont(QFont("Arial", 11))
        layout.addWidget(self.label)
        
        self.port_combo = QComboBox()
        self.port_combo.setFont(QFont("Arial", 10))
        layout.addWidget(self.port_combo)
        
        # Baud rate selection
        baud_layout = QHBoxLayout()
        self.baud_label = QLabel("Baud Rate:")
        self.baud_label.setFont(QFont("Arial", 11))
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.baud_combo.setCurrentText("115200") #default value baudrate 115200
        baud_layout.addWidget(self.baud_label)
        baud_layout.addWidget(self.baud_combo)
        layout.addLayout(baud_layout)
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh Ports")
        self.refresh_button.clicked.connect(self.populate_ports)
        layout.addWidget(self.refresh_button)
        
        # OK/Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                           QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
        self.setLayout(layout)
        self.populate_ports()
    
    def populate_ports(self):
        """Find all available serial ports"""
        self.port_combo.clear()
        ports = sorted(list_ports.comports())
        
        if not ports:
            self.port_combo.addItem("No ports found")

            #self.button_box.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False) <-- Disables OK button (will remove at the end)
            
            #Create last check if you want programed launched
            #Create program launch without port --> Placeholder data


        else:
            for port, desc, hwid in ports:
                self.port_combo.addItem(f"{port} - {desc}")
            self.button_box.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)
    
    def get_selected_port(self):
        """Return the currently selected port"""
        if self.port_combo.currentText() == "No ports found":
            return None
        return self.port_combo.currentText().split(" - ")[0]
    
    def get_selected_baudrate(self):
        """Return the selected baud rate as an integer"""
        return int(self.baud_combo.currentText())
    
    def accept(self):
        print("=" * 50)
        print("OK BUTTON WAS CLICKED!")
        print("=" * 50)
        super().accept()
    
    def reject(self):
        print("Canceling program launch...")
        sys.exit()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     dialog = PortSelectionDialog()
    
#     if dialog.exec():
#         port = dialog.get_selected_port()
#         baudrate = dialog.get_selected_baudrate()
#         print(f"Selected: {port} at {baudrate} baud")
    
#     sys.exit()
#Not needed because of implementation in main