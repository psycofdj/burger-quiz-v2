import os
import yaml
from PySide6 import QtCore, QtWidgets
from bquiz.types import Team

class Match(QtCore.QObject):
    def __init__(self, hw, widget = None):
        super().__init__(widget)
        self.pageNum = None
        self.leader = None
        self.mayoScore = 0
        self.ketchupScore = 0
        self.frame = self.getFrame(widget)
        self.frame.hide()

    def clone(self, match):
        self.leader = match.leader
        self.mayoScore = match.mayoScore
        self.ketchupScore = match.ketchupScore
        self.frame.update()

    def reset(self):
        self.leader = None
        self.mayoScore = 0
        self.ketchupScore = 0
        self.pageNum = None
        self.frame.update()

    def setPageNum(self, num):
        self.pageNum = num
        self.frame.update()

    @staticmethod
    def readFile(name):
        root = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(root, "resources", name)
        with open(path) as f:
            return yaml.safe_load(f)

    def getFrame(self, widget):
        return BaseFrame(self, widget)

    def setLeader(self, team):
        self.leader = team
        self.frame.update()

    def setScore(self, mayoScore, ketchupScore):
        self.mayoScore = max(0, mayoScore)
        self.ketchupScore = max(0, ketchupScore)
        self.frame.update()

    @QtCore.Slot()
    def setMayoLeader(self):
        self.setLeader(Team.MAYO)

    @QtCore.Slot()
    def setKetchupLeader(self):
        self.setLeader(Team.KETCHUP)

    def hideError(self):
        self.frame.error.hide()

    @QtCore.Slot(str)
    def ephemeralError(self, txt):
        self.frame.error.setText(txt)
        self.frame.error.raise_()
        self.frame.error.show()
        QtCore.QTimer.singleShot(5000, self.hideError)

    def resourcePath(self, filename):
        return self.frame.resourcePath(filename)
