import sys
import os
from bquiz.hardware import Hardware
from bquiz.game.engine import Engine
from bquiz.mock import Mock
from bquiz.data import data

from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow
)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedWidth(800)
        self.setFixedHeight(480)
        if not "--mock" in sys.argv:
            self.hw = Hardware(self)
        else:
            self.hw = Mock()
            self.hw.move(860, 0)
            self.hw.show()
        self.engine = Engine(self.hw, self)
        self.hw.spawn()

    def keyPressEvent(self, event):
        want = QtCore.QKeyCombination(QtCore.Qt.ControlModifier, QtCore.Qt.Key_C)
        if event.keyCombination() == want:
            sys.exit(1)

def main():
    sys.stdout = sys.stderr
    app = QApplication(sys.argv)
    if not "--mock" in sys.argv:
        cursor = QtGui.QCursor(QtCore.Qt.BlankCursor);
        app.setOverrideCursor(cursor);
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
