from PySide6 import QtCore, QtWidgets

from bquiz.game.match import Match

class Question(Match):
    def __init__(self, hw, widget = None):
        super().__init__(hw, widget)
        self.questions = []
        hw.mayoPlusBtn.pressed.connect(self.incMayoScore)
        hw.mayoMinusBtn.pressed.connect(self.decMayoScore)
        hw.ketchupPlusBtn.pressed.connect(self.incKetchupScore)
        hw.ketchupMinusBtn.pressed.connect(self.decKetchupScore)

    def reset(self):
        super().reset()
        self.setQ(0, 0)

    def nextQ(self):
        self.setQ(self.nextIndex, self.nextPos)

    def prevQ(self):
        self.setQ(self.prevIndex, self.prevPos)

    def setQ(self, index, pos):
        self.prevIndex = max(index - 1, 0)
        self.prevPos = 0
        self.nextIndex = min(index + 1, len(self.questions) - 1)
        self.nextPos = 0

        hasNext, nextPos = self.frame.setItem(index, self.questions[index], pos)
        self.setPageNum(self.questions[index].get("id", None))

        if hasNext:
            self.nextIndex = index
            self.nextPos = nextPos
            self.frame.useAltBg()
        else:
            self.frame.useBg()

        if index == len(self.questions) - 1 and pos != 0:
            self.nextIndex = index
            self.nextPos = pos

    @QtCore.Slot()
    def incMayoScore(self):
        self.setScore(self.mayoScore + 1, self.ketchupScore)

    @QtCore.Slot()
    def incKetchupScore(self):
        self.setScore(self.mayoScore, self.ketchupScore + 1)

    @QtCore.Slot()
    def decMayoScore(self):
        self.setScore(self.mayoScore -1, self.ketchupScore)

    @QtCore.Slot()
    def decKetchupScore(self):
        self.setScore(self.mayoScore, self.ketchupScore - 1)
