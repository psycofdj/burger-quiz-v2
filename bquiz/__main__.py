from .app import App
from .game.toss import Toss

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow
)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedWidth(800)
        self.setFixedHeight(480)
        self.w = Toss(self)
        self.setCentralWidget(self.w)
        self.hw = App(self)
        self.hw.resetBtn.pressed.connect(self.w.randomTos)
        self.hw.mayoPlusBtn.pressed.connect(self.w.frame.setMayoLeader)
        self.hw.mayoMinusBtn.pressed.connect(self.w.frame.setMayoLeader)
        self.hw.ketchupPlusBtn.pressed.connect(self.w.frame.setKetchupLeader)
        self.hw.ketchupMinusBtn.pressed.connect(self.w.frame.setKetchupLeader)
        self.hw.spawn()

def run():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


def main():
    run()

if __name__ == "__main__":
    main()

# from .app import App
# from .gui import run

# def main():
#     app = App()
#     thread = app.spawn()
#     run()
#     thread.join()

# if __name__ == "__main__":
#     main()
