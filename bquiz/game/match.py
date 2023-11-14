import os
import subprocess
import yaml
from PySide6 import QtCore, QtWidgets
from bquiz.types import Team

class Match(QtCore.QObject):
    def __init__(self, hw, widget = None):
        super().__init__(widget)
        self.hw = hw
        self.pageNum = None
        self.leader = None
        self.mayoScore = 0
        self.ketchupScore = 0
        self.volume = self.getSystemVolume()
        self.frame = self.getFrame(widget)
        self.frame.hide()
        self.frame.longClick.connect(self.volumeShow)
        self.frame.click.connect(self.volumeHide)
        self.frame.volumeMinus.clicked.connect(self.volumeMinus)
        self.frame.volumePlus.clicked.connect(self.volumePlus)


    def finalize(self):
        pass

    def clone(self, match):
        self.leader = match.leader
        self.mayoScore = match.mayoScore
        self.ketchupScore = match.ketchupScore
        self.volume = match.volume
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

    def getSystemVolume(self):
        out = subprocess.check_output(['/bin/bash', '-c', "amixer -D pulse sget Master | grep 'Left:' | awk -F'[][]' '{ print $2 }'"])
        vol = out.decode('utf-8').split("%")[0]
        return int(vol)

    def setVolume(self, val):
        self.volume = max(min(val, 85), 0)
        cmd = "amixer -q set Master %d%%" % (self.volume)
        os.system(cmd)
        self.frame.update()

    @QtCore.Slot()
    def volumeShow(self):
        self.frame.volumeBox.raise_()
        self.frame.volumeBox.show()

    @QtCore.Slot()
    def volumeHide(self):
        self.frame.volumeBox.hide()

    @QtCore.Slot()
    def volumePlus(self):
        self.setVolume(self.volume + 5)

    @QtCore.Slot()
    def volumeMinus(self):
        self.setVolume(self.volume - 5)
