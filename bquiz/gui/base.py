import os
from PySide6 import QtCore, QtWidgets
from bquiz.types import Team

class BaseFrame(QtWidgets.QFrame):
    def __init__(self, handler, parent = None):
        super().__init__(parent)
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

        self.image = "base.png"
        self.color = "#cccccc"
        self.ketchup.setText(str(self.handler.ketchupScore))
        self.mayo.setText(str(self.handler.mayoScore))
        self.page.setText("")
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

    def reset(self):
        self.ketchup.setText(str(self.handler.ketchupScore))
        self.mayo.setText(str(self.handler.mayoScore))
        self.page.setText("")
        self.updateStyle()

    def setBackgound(self, image, color):
        self.image = image
        self.color = color
        self.updateStyle()
