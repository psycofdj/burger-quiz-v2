import random
import sys
import yaml

from PySide6 import (
    QtWidgets,
    QtGui,
    QtCore,
)

from PySide6.QtCore import (
    Qt,
    Slot,
)

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QSizePolicy,
)

from PySide6.QtGui import (
    QFont,
    QImage,
    QPainter,
    QPixmap,
    QPen,
)
import os

def log(arg):
    print(str(arg))
    with open("/tmp/log", "a") as f:
        f.write(str(arg) + "\n")

class DefaultRenderer:
    def __init__(self, item, initialPos):
        self.initialPos = initialPos
        self.title = item.get("title", "")
        self.subtitle = item.get("subtitle", None)
        self.questions = item.get("questions", [])
        self.size = item.get("size", "normal")
        self.maxHeight = 406

    def renderTitle(self):
        if self.initialPos != 0 or not self.title:
            # no title for back page
            return ""
        inner = """<b>%s</b>""" % (self.title)
        if self.subtitle:
            inner = """<b>%s</b><br/><i>%s</i>""" % (self.title, self.subtitle)
        return """<div class="title">%(inner)s</div>""" % {
            "inner": inner
        }

    def renderQuestion(self, qItem):
        q = qItem.get("Q", "<missing>")
        a = qItem.get("A", "<missing>")
        return """
        <li>
          %(Q)s.<br/><span class="answer">%(A)s</span>
        </li>""" % qItem

    def renderQuestions(self, questions):
        return """
        <div class="q">
          <ul>
          %(q)s
          </ul>
        </div>""" % {
            "q": "\n".join([ self.renderQuestion(x) for x in questions ])
        }

    def renderStyles(self):
        sizes = { "title": "28px", "q": "25px" }
        if self.size == "small":
            sizes = { "title": "22px", "q": "18px" }
        if self.size == "medium":
            sizes = { "title": "26px", "q": "22px" }
        return """
         <style>
          .title  { font-size: %(sizes.title)s; }
          .q      { font-size: %(sizes.q)s; }
          .answer { color: red; }
        </style>
        """ % {
            "sizes.title": sizes['title'],
            "sizes.q": sizes['q'],
        }

    def renderChunk(self, chunk):
        styles = self.renderStyles()
        title = self.renderTitle()
        questions = self.renderQuestions(chunk)
        return """
        %(styles)s
        %(title)s
        %(questions)s
        """ % {
            "styles": styles,
            "title": title,
            "questions": questions,
        }

    @staticmethod
    def createLabel():
        font = QtGui.QFont("Ubuntu")
        font.setStretch(QtGui.QFont.ExtraCondensed)
        label = QLabel(None)
        label.setFont(font)
        label.setFixedWidth(800)
        label.setTextFormat(Qt.TextFormat.RichText)
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        return label

    def isValid(self, label, text):
        doc = QtGui.QTextDocument(None)
        doc.setHtml(text)
        doc.setDefaultFont(label.font())
        doc.setTextWidth(800 - 55 - 135)
        size = doc.documentLayout().documentSize()
        if size.height() > self.maxHeight:
            return False
        label.setText(text)
        return True

    def finalize(self, label, pos):
        hasNext = (pos < len(self.questions) - 1)
        return label, hasNext, pos

    def chunkQ(self, label):
        qCount = 0
        qIdx = self.initialPos
        maxIdx = len(self.questions)
        if self.initialPos == 0:
            # max half of question per page
            maxIdx = maxIdx/2
        while qIdx+qCount < maxIdx:
            qCount += 1
            qSubset = self.questions[qIdx:qIdx+qCount]
            text = self.renderChunk(qSubset)
            if not self.isValid(label, text):
                break
        return self.finalize(label, qIdx+qCount)

    def render(self):
        label = self.createLabel()
        text = self.renderChunk(self.questions)
        if self.initialPos != 0 or not self.isValid(label, text):
            return self.chunkQ(label)
        return self.finalize(label, len(self.questions) - 1)


class AdditionRenderer(DefaultRenderer):
    def __init__(self, item, initialPos):
        DefaultRenderer.__init__(self, item, initialPos)

class SelPoivreRenderer(DefaultRenderer):
    def __init__(self, item, initialPos):
        DefaultRenderer.__init__(self, item, initialPos)

class NuggetsRenderer(DefaultRenderer):
    def __init__(self, item, initialPos):
        DefaultRenderer.__init__(self, item, initialPos)

    def renderStyles(self):
        sizes = { "q": "22px" }
        return """
         <style>
          .q      { font-size: %(sizes.q)s; }
          .answer { color: red; }
         </style>
        """ % {
            "sizes.q": sizes['q'],
        }

    def renderChoice(self, value, isAnswer):
        itemClass = ""
        if isAnswer:
            itemClass = "answer"
        return """
          <li class="%(class)s">%(value)s</li>
        """ % {
            'class': itemClass,
            'value': value,
        }

    def renderQuestion(self, qItem, idx):
        choices = ['A', 'B', 'C', 'D']
        answer = qItem.get('answer', None)
        def isValid(choice):
            if type(answer) == list:
                return choice in answer
            return choice == answer
        items = [ self.renderChoice(qItem['choices'].get(x, ""), isValid(x)) for x in choices ]
        return """
        <li>
          <b>%(idx)s. %(Q)s</b>
          <ul>
            %(items)s
          </ul>
        </li>
        """ % {
            'idx': self.initialPos + idx + 1,
            'Q': qItem.get('question', ""),
            'items': "\n".join(items),
        }

    def renderQuestions(self, questions):
        return """
        <div class="q">
        %(q)s
        </div>""" % {
            "q": "<br/>".join([ self.renderQuestion(val, idx) for idx,val in enumerate(questions) ])
        }

    def render(self):
        label = self.createLabel()
        if self.initialPos == 0:
            questions = self.questions[0:2]
        else:
            questions = self.questions[2:4]
        text = self.renderChunk(questions)
        label.setText(text)
        return self.finalize(label, self.initialPos + 2)

class MenusRenderer(DefaultRenderer):
    def __init__(self, item, initialPos):
        DefaultRenderer.__init__(self, item, initialPos)
        self.sizes = [ "normal", "medium", "small", "xsmall" ]

    def renderStyles(self):
        sizes = { "title": "28px", "q": "25px" }
        if self.size == "medium":
            sizes = { "title": "26px", "q": "22px" }
        if self.size == "small":
            sizes = { "title": "22px", "q": "18px" }
        if self.size == "xsmall":
            sizes = { "title": "22px", "q": "16px" }
        return """
         <style>
          .title  { font-size: %(sizes.title)s; }
          .q      { font-size: %(sizes.q)s; }
          .answer { color: red; }
        </style>
        """ % {
            "sizes.title": sizes['title'],
            "sizes.q": sizes['q'],
        }

    def render(self):
        idx = 0
        label = self.createLabel()
        text = self.renderChunk(self.questions)
        while not self.isValid(label, text) and idx < len(self.sizes):
            idx += 1
            self.size = self.sizes[idx]
            text = self.renderChunk(self.questions)
        label.setText(text)
        return self.finalize(label, len(self.questions) - 1)

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.config = {
            "nuggets" : {
                "bg-color": "#ffff8d",
                "file": "nuggets.yaml",
                "renderer": NuggetsRenderer,
                "bg": 'nuggets-back.png',
                "bg-arrow": 'nuggets-back.png',
            },
            "selpoivre": {
                "bg-color": "#d4bee4",
                "file": "selpoivre.yaml",
                "bg": 'selpoivre-back.png',
                "bg-arrow": 'selpoivre-back-arrow.png',
                "renderer": SelPoivreRenderer,
            },
            "menus": {
                "bg-color": "#cfffff",
                "file": "menus.yaml",
                "renderer": MenusRenderer,
                "bg": 'menus-back.png',
                "bg-arrow": 'menus-back-arrow.png',
            },
            "menus-rouge": {
                "bg-color": "#ffd38f",
                "file": "menus-rouge.yaml",
                "renderer": MenusRenderer,
                "bg": 'menus-rouge-back.png',
                "bg-arrow": 'menus-rouge-back.png',
            },
            "addition": {
                "bg-color": "#ff9d82",
                "file": "addition.yaml",
                "renderer": AdditionRenderer,
                "bg": 'addition-back.png',
                "bg-arrow": 'addition-back-arrow.png',
            }
        }
        self.current = "menus-rouge"
        path = os.path.join(os.path.dirname(__file__), "resources", self.config[self.current]["file"])
        with open(path) as f:
            self.data = yaml.safe_load(f)
        QtWidgets.QMainWindow.__init__(self)
        self.qIndex = 0
        self.qPos = 0
        self.setFixedWidth(800)
        self.setFixedHeight(480)
        self.setBackgroundImage(False)
        self.setQ(self.qIndex, self.qPos)

    def setBackgroundImage(self, arrow):
        name = self.config[self.current]['bg']
        if arrow:
            name = self.config[self.current]['bg-arrow']
        path = os.path.join(os.path.dirname(__file__), "resources", name)
        style = """
        QMainWindow {
          border-image: url("%(path)s");
          background-color: %(bg-color)s;
        }
        QLabel {
          margin: 40px 55px 43px 135px;
        }""" % {
            'path': path,
            'bg-color': self.config[self.current]['bg-color'],
        }
        self.setStyleSheet(style)

    def nextQ(self):
        self.setQ(self.nextIndex, self.nextPos)

    def prevQ(self):
        self.setQ(self.prevIndex, self.prevPos)

    def setQ(self, index, pos):
        self.prevIndex = max(index - 1, 0)
        self.prevPos = 0
        if pos != 0:
            self.prevIndex = self.qIndex
            self.prevPos = 0
        self.qIndex = index
        self.qPos = pos
        renderer = self.config[self.current]['renderer'](self.data[self.qIndex], self.qPos)
        self.label, hasNext, nextPos = renderer.render()
        if hasNext:
            self.setBackgroundImage(True)
            self.nextIndex = self.qIndex
            self.nextPos = nextPos
        else:
            self.setBackgroundImage(False)
            if (self.qIndex + 1) != len(self.data):
                self.nextIndex = self.qIndex + 1
                self.nextPos = 0

        self.pageNum = QLabel(self.label)
        self.pageNum.setText("<b>%s</b>" % (self.qIndex+1))
        self.pageNum.setMinimumHeight(110)
        self.pageNum.setMinimumWidth(75)
        self.pageNum.move(630, 400)
        self.pageNum.setStyleSheet("QLabel { color: %(color)s }" % {
            "color": self.config[self.current]["bg-color"],
        })
        self.label.setParent(self)
        self.setCentralWidget(self.label)
        self.setWindowFlag(Qt.FramelessWindowHint)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            sys.exit(0)
        if event.key() == Qt.Key_Right:
            self.nextQ()
        if event.key() == Qt.Key_Left:
            self.prevQ()

    def mousePressEvent(self, event):
        if event.pos().x() > self.width() / 2:
            self.nextQ()
        else:
            self.prevQ()

def run():
    app = QApplication(sys.argv)
    cursor = QtGui.QCursor(Qt.BlankCursor);
    app.setOverrideCursor(cursor);
    widget = MyWindow()
    widget.show()
    sys.exit(app.exec_())
