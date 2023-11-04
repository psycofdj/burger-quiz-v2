import os
from PySide6 import QtCore, QtWidgets
from bquiz.types import Team

class BaseFrame(QtWidgets.QFrame):
    def __init__(self, bg, altBg, color, handler, widget = None):
        super().__init__(widget)
        self.handler = handler
        self.setObjectName("mainFrame")

        self.ketchup = QtWidgets.QLabel(self)
        self.ketchup.setObjectName("ketchup")
        self.ketchup.setGeometry(5, 5, 50, 50)
        self.ketchup.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

        self.mayo = QtWidgets.QLabel(self)
        self.mayo.setObjectName("mayo")
        self.mayo.setGeometry(745, 5, 50, 50)
        self.mayo.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

        self.page = QtWidgets.QLabel(self)
        self.page.setObjectName("page")
        self.page.setGeometry(745, 425, 50, 50)
        self.page.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

        self.bg = bg
        self.altBg = altBg
        self.color = color
        self.image = "base.png"
        self.ketchup.setText(str(self.handler.ketchupScore))
        self.mayo.setText(str(self.handler.mayoScore))
        self.page.setText("")

        self.error = QtWidgets.QLabel(self)
        self.error.setObjectName("error")
        self.error.setGeometry(100, 240-50, 600, 100)
        self.error.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.error.setText("")
        self.error.hide()

        self.useBg()
        self.updateStyle()

    def getTeamStyle(self, team):
        config = {
            Team.MAYO: "#ffb328",
            Team.KETCHUP: "#bb0000",
        }
        if team == self.handler.leader:
            return """
            QLabel#%(name)s {
              background-color: %(color)s;
              color: black;
              font-weight:600;
              border-radius: 10px
            }
            """ % {
                "name": team.name.lower(),
                "color": config[team]
            }
        return """
        QLabel#%(name)s {
          color: %(color)s;
          font-weight:600;
        }
        """ % {
            "name": team.name.lower(),
            "color": config[team]
        }

    def updateStyle(self):
        root = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(root, "resources", self.image)
        style = """
        QLabel#page, QLabel#mayo, QLabel#ketchup {
          font-family: Ubuntu;
          font-size: 30px;
        }
        QLabel#page {
          color: %(bg-color)s;
        }
        QLabel#error {
          font-size: 20px;
          color: white;
          background: back;
          border: 5px solid red;
          border-radius: 30px;
        }
        QFrame#mainFrame {
          border-image: url("%(path)s");
          background-color: %(bg-color)s;
        }
        %(mayo)s
        %(ketchup)s
        """ % {
            'path': path,
            'bg-color': self.color,
            'mayo': self.getTeamStyle(Team.MAYO),
            'ketchup': self.getTeamStyle(Team.KETCHUP),
        }
        self.setStyleSheet(style)
        self.setFixedWidth(800)
        self.setFixedHeight(480)

    def update(self):
        self.ketchup.setText(str(self.handler.ketchupScore))
        self.mayo.setText(str(self.handler.mayoScore))
        if self.handler.pageNum is not None:
            self.page.setText(str(self.handler.pageNum))
        self.error.setText("")
        self.error.hide()
        self.updateStyle()

    def useBg(self):
        self.image = self.bg
        self.updateStyle()

    def useAltBg(self):
        self.image = self.altBg
        self.updateStyle()

    def setColor(self, color):
        self.color = color
        self.updateStyle()
