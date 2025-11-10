
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import sys

class Graph(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acceleration Y Graph")
        self.setGeometry(100, 100, 1200, 700)

        self.df = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        controls_layout = QHBoxLayout()

        self.load_btn = QPushButton("Load CSV File")
        self.load_btn.clicked.connect(self.load_csv)
        controls_layout.addWidget(self.load_btn)

        # controls_layout.addWidget(QLabel("Time Column: "))
        # self.time_combo = QComboBox()
        # self.time_combo.setEnabled(False)
        # controls_layout.addWidget(self.time_combo)

        # controls_layout.addWidget(QLabel("Value Column: "))
        # self.value_combo = QComboBox()
        # self.value_combo.setEnabled(False)
        # controls_layout.addWidget(self.value_combo)

        self.plot_btn = QPushButton("Plot Graph")
        self.plot_btn.clicked.connect(self.plot_graph)
        self.plot_btn.setEnabled(False)
        controls_layout.addWidget(self.plot_btn)

        layout.addLayout(controls_layout)

        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if not file_path:
            return
        try:
            self.df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Failed to read CSV: {e}")
            return

        print(f"Loaded CSV: {file_path}")
        print(f"Rows: {len(self.df)} Columns: {list(self.df.columns)}")

        self.plot_btn.setEnabled(True)

    def plot_graph(self):
        if self.df is None:
            print("Data is not loaded!")
            return

        time_col = "time_elapsed"
        value_col = "acceleration_y"

        # __ over ___ function
        if time_col not in self.df.columns or value_col not in self.df.columns:
            print(f"Required columns not found: need '{time_col}' and '{value_col}'")
            return


        try:
            self.figure.clear()
            subp = self.figure.add_subplot(111)
            subp.plot(self.df[time_col], self.df[value_col], marker='o', linestyle='-')
            subp.set_xlabel(time_col)
            subp.set_ylabel(value_col)
            subp.set_title(f"{value_col} over {time_col}")
            subp.tick_params(axis='x', rotation=45)
            self.figure.tight_layout()
            self.canvas.draw()
            print("graph has been successfully plotted!")
        except Exception as e:
            print(f"Error plotting: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Graph()
    window.show()
    sys.exit(app.exec())
