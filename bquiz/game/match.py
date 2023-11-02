from PySide6 import QtCore, QtWidgets
from bquiz.types import Team

class Match(QtCore.QObject):
    def __init__(self, hw, parent = None):
        super().__init__(parent)
        self.hw = hw
        self.leader = None
        self.mayoScore = 0
        self.ketchupScore = 0
        self.frame = self.getFrame()
        print("test debug")

    def reset(self):
        self.leader = None
        self.mayoScore = 0
        self.ketchupScore = 0
        self.frame.reset()

    def getFrame(self):
        return BaseFrame(self)

    def setLeader(self, team):
        self.leader = team
        self.frame.reset()

    @QtCore.Slot()
    def setMayoLeader(self):
        self.setLeader(Team.MAYO)

    @QtCore.Slot()
    def setKetchupLeader(self):
        self.setLeader(Team.KETCHUP)
