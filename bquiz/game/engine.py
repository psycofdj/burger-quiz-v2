from PySide6 import QtCore, QtWidgets

from bquiz.game.toss import Toss

class Engine(QtCore.QObject):
    def __init__(self, hw, parent = None):
        super().__init__(parent)
        self.mainWindow = parent
        self.hw = hw
        self.hw.resetBtn.longPressed.connect(self.reset)
        self.hw.nuggetsBtn.pressed.connect(self.startNuggets)
        self.hw.menusBtn.pressed.connect(self.startMenus)
        self.hw.additionBtn.pressed.connect(self.startAddition)
        self.toss = Toss(self.hw, self)
        self.mainWindow.setCentralWidget(self.toss.frame)

    @QtCore.Slot()
    def reset(self):
        self.toss.reset()
        self.mainWindow.setCentralWidget(self.toss.frame)

    @QtCore.Slot()
    def startNuggets(self):
        self.toss.hide()

    @QtCore.Slot()
    def startSelPoivre(self):
        self.reset()

    @QtCore.Slot()
    def startMenus(self):
        self.toss.hide()

    @QtCore.Slot()
    def startAddition(self):
        self.toss.hide()
