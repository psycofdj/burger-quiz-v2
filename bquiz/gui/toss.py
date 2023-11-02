from PySide6 import QtCore, QtWidgets

from .base import BaseFrame


class TossFrame(BaseFrame):
    INTRO = """
<style>
* {
  font-familly: Ubuntu;
}
.r {
  background-color:#bb0000;
  color:white;
  padding:2px;
  font-familly: Monospace
}
.r2 {
  background-color:#bb0000;
  color:black;
  padding:2px;
  font-familly: Monospace
}
.y {
  background-color:#ffb328;
  color:white;
  padding:2px;
  font-familly: Monospace
}
.b {
  background-color:blue;
  color: #cfffff;
  padding:2px;
  font-familly: Monospace
}
</style>

<center>
    <p>Bonjour et bienvenu au <b class="b">B</b> <b class="b">U</b> <b class="b">R</b> <b class="b">G</b> <b class="b">E</b> <b class="b">R</b>&nbsp;&nbsp;<b class="r">Q</b> <b class="y">U</b> <b class="r">I</b> <b class="y">Z</b> !</b></p>
</center>
<p>
    <b class="r2">J</b>e propose aux équipes Mayo et Ketchup de s'affronter dans une serie de 4 épreuves dans
    lesquelles il vous faudra récolter un maximum de Miam: <b>Nuggets, Sel ou poivre, Les menus</b>
    et enfin <b>l'Addition</b>.
</p>
<p>
    <b class="r2">D</b>eux sont des épreuves de rapidité où il vous foudra buzzer, les deux autres seront équipes
    par équipes. Tout buzz intempestif est à proscrire sous peine de pénalité.
    Quand à moi je serai votre hôte: le grand Miam.
</p>
<p>
    <b class="r2">P</b>our commencer je vais vous demander de nommer un chef dans chacunes des équipes, et pour
    déterminer celui qui commencer, les chefs vont s'affronter sur un petit toss.
</p>"""
    def __init__(self, parent = None):
        BaseFrame.__init__(self, parent)
        self.setBackgound("base.png", "#000000")

        self.tos = QtWidgets.QLabel(self)
        self.tos.setObjectName("tos")
        self.tos.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.tos.setGeometry(55, 55+480-110-75, 800-110, 75)
        self.tos.setWordWrap(True)
        self.tos.setTextFormat(QtCore.Qt.RichText)
        self.tos.setStyleSheet("")
        self.tos.setText("")
        self.tos.setStyleSheet("""
        QLabel {
          color: #ffb328;
          font-size: 22px;
          font-weight:600;
        }
        """)

        self.static = QtWidgets.QLabel(self)
        self.static.setObjectName("static")
        self.static.setAlignment(QtCore.Qt.AlignVCenter)
        self.static.setGeometry(55, 55, 800-110, 480-110-75)
        self.static.setWordWrap(True)
        self.static.setTextFormat(QtCore.Qt.RichText)
        self.static.setStyleSheet("""
        QLabel {
          color: white;
          font-size: 19px;
        }
        """)
        self.static.setText(TossFrame.INTRO)


    @QtCore.Slot(str)
    def setTos(self, value):
        self.tos.setText(value)

