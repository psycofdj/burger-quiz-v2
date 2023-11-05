import time
import yaml
import random

from PySide6  import QtCore

from bquiz.data import data
from bquiz.game.question import Question
from bquiz.gui.menus import MenusFrame

class Menus(Question):
    def __init__(self, hw, widget = None):
        super().__init__(hw, widget)
        self.menus = data['menus']
        self.menusRouge = data['menus-rouge']
        self.randomQ()
        self.hw.resetBtn.pressed.connect(self.randomQ)

    def finalize(self):
        self.hw.resetBtn.pressed.disconnect(self.randomQ)
        super().finalize()

    def getFrame(self, widget):
        return MenusFrame(self, widget)

    def reset(self):
        super().reset()
        self.randomQ()

    @QtCore.Slot()
    def randomQ(self):
        random.seed(time.time())
        idx1 = random.randrange(0, len(self.menus), 1)
        idx2 = (idx1 + 1) % len(self.menus)
        rIdx = random.randrange(0, len(self.menusRouge), 1)
        self.questions = [ self.menus[idx1], self.menus[idx2], self.menusRouge[rIdx] ]
        self.setQ(0, 0)
