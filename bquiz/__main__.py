import sys
from bquiz.hardware import Hardware
from bquiz.game.engine import Engine

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow
)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedWidth(800)
        self.setFixedHeight(480)
        self.hw = Hardware(self)
        self.engine = Engine(self.hw, self)
        self.hw.spawn()

def main():
    sys.stdout = sys.stderr
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
