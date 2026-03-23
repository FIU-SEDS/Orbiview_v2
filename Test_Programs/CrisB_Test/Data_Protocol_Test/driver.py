from PyQt6.QtWidgets import QApplication, QWidget

class MainWindow():
    def __init__(self):
        super().__init__()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()