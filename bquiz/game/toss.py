import random

from PySide6  import QtCore

from .match import Match
from bquiz.gui.toss import TossFrame
from bquiz.types import Team

class Toss(Match):
    tos_changed = QtCore.Signal(str)
    has_winner = QtCore.Signal(Team)
    def __init__(self, parent = None):
        Match.__init__(self, parent)
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
        self.tosIdx = 0
        self.randomTos()
        self.frame = TossFrame(self)
        self.tos_changed.connect(self.frame.setTos)
        self.randomTos()

    def setTos(self, idx):
        idx = idx % len(self.data)
        self.tos = self.data[idx]
        self.tos_changed.emit(self.tos)

    @QtCore.Slot()
    def randomTos(self):
        self.setTos(random.randrange(0, len(self.data), 1))

    @QtCore.Slot()
    def mayoPressed(self):
        self.winner = Team.MAYO
        self.has_winner.emit(self.winner)

    @QtCore.Slot()
    def ketchupPressed(self):
        self.winner = Team.MAYO
        self.has_winner.emit(self.winner)
