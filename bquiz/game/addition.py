import time
import yaml
import random

from PySide6  import QtCore

from bquiz.data import data
from bquiz.game.question import Question
from bquiz.gui.addition import AdditionFrame

class Addition(Question):
    def __init__(self, hw, widget = None):
        super().__init__(hw, widget)
        self.data = data['addition']
        self.randomQ()
        self.hw.resetBtn.pressed.connect(self.randomQ)

    def finalize(self):
        self.hw.resetBtn.pressed.disconnect(self.randomQ)
        super().finalize()

    def getFrame(self, widget):
        return AdditionFrame(self, widget)

    def reset(self):
        super().reset()
        self.randomQ()

    @QtCore.Slot()
    def randomQ(self):
        random.seed(time.time())
        idx = random.randrange(0, len(self.data), 1)
        self.questions = [ self.data[idx] ]
        self.setQ(0, 0)
