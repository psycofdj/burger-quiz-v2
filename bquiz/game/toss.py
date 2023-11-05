import random

from PySide6  import QtCore

from bquiz.game.match import Match
from bquiz.gui.toss import TossFrame
from bquiz.types import Team

class Toss(Match):
    tosChanged = QtCore.Signal(str)
    def __init__(self, hw, widget = None):
        super().__init__(hw, widget)
        x, y, z, u = (
            random.randrange(1, 99, 1),
            random.randrange(1, 99, 1),
            random.randrange(1, 99, 1),
            random.randrange(1, 99, 1)
        )
        self.data = [
            "Faire un shi-fu-mi sur 1 manche",
            "Chou-fleur, 6m, mayo demarre, talons collés aux pointes",
            "Le plus proche du resultat: %d * %d * %d / %d = %d" % (
                x, y, z, u, x * y * z / u,
            ),
            "Quelle main ? (cacher un doigt d'honneur)",
            "Ping pong, theme: film avec Tom Cruise",
            "Ping pong, theme: films avec Stallone",
            "Ping pong, theme: mots commencant par hypo",
            "Ping pong, theme: animal a 4 pattes",
            "Celui tenant le plus longtemps en equilibre sur une jambe",
            "Faire un je te tiens par la barbichette",
            "La pire resolution du nouvel an",
            "Le premier qui cligne des yeux a perdu",
            "Celui qui imite le mieux la Joconde",
            "Celui qui imite le mieux un chien ayant mange un canard",
            "Celui qui fait le mieux samblant de parler Russe",
            "Celui qui fait le plus long oooooommmmmmmmmmm",
        ]
        hw.resetBtn.pressed.connect(self.randomToss)
        hw.mayoPlusBtn.pressed.connect(self.setMayoLeader)
        hw.mayoMinusBtn.pressed.connect(self.setMayoLeader)
        hw.ketchupPlusBtn.pressed.connect(self.setKetchupLeader)
        hw.ketchupMinusBtn.pressed.connect(self.setKetchupLeader)
        self.randomToss()

    def getFrame(self, widget):
        return TossFrame(self, widget)

    def reset(self):
        super().reset()
        self.randomToss()

    def setToss(self, idx):
        self.frame.setToss(self.data[idx % len(self.data)])

    @QtCore.Slot()
    def randomToss(self):
        self.setToss(random.randrange(0, len(self.data), 1))
