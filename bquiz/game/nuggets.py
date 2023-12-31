import random
import time
from PySide6  import QtCore
from bquiz.data import data
from bquiz.game.question import Question
from bquiz.gui.nuggets import NuggetsFrame

class Nuggets(Question):
    def __init__(self, hw, widget = None):
        super().__init__(hw, widget)
        self.data = data['nuggets']
        self.randomQ()
        self.hw.resetBtn.pressed.connect(self.randomQ)

    def finalize(self):
        self.hw.resetBtn.pressed.disconnect(self.randomQ)
        super().finalize()

    def getFrame(self, widget):
        return NuggetsFrame(self, widget)

    @QtCore.Slot()
    def randomQ(self):
        random.seed(time.time())
        idx1 = random.randrange(0, len(self.data), 1)
        idx2 = (idx1 + 1) % len(self.data)
        self.questions = [ self.data[idx1], self.data[idx2] ]
        self.setQ(0, 0)

    def reset(self):
        super().reset()
        self.randomQ()
