import time
import yaml
import random

from PySide6  import QtCore

from bquiz.game.question import Question
from bquiz.gui.selpoivre import SelPoivreFrame

class SelPoivre(Question):
    def __init__(self, hw, widget = None):
        super().__init__(hw, widget)
        self.data = self.readFile("selpoivre.yaml")
        self.randomQ()
        hw.resetBtn.pressed.connect(self.randomQ)

    def getFrame(self, widget):
        return SelPoivreFrame(self, widget)

    def reset(self):
        super().reset()
        self.randomQ()

    @QtCore.Slot()
    def randomQ(self):
        random.seed(time.time())
        idx = random.randrange(0, len(self.data), 1)
        self.questions = [ self.data[idx] ]
        self.setQ(0, 0)
