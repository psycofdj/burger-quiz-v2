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

class AdditionRenderer:
    def __init__(self, item, initialPos):
        self.initialPos = initialPos
        self.title = item.get("title", "")
        self.subtitle = item.get("subtitle", None)
        self.questions = item.get("questions", [])
        self.size = item.get("size", "normal")
        self.maxHeight = 400
    @staticmethod
    def formatTitle(title, subtitle):
        if subtitle:
            return """<b>%s</b><br/><i>%s</i>""" % (title, subtitle)
        return """<b>%s</b>""" % (title)

    @staticmethod
    def formatQuestion(qItem):
        q = qItem["Q"]
        a = qItem["A"]
        return """<li> %(Q)s.<br/><span class="answer">%(A)s</span></li>""" % qItem

    def formatText(self, questions):
        sizes = { "title": "28px", "q": "25px" }
        if self.size == "small":
            sizes = { "title": "22px", "q": "18px" }
        if self.size == "medium":
            sizes = { "title": "26px", "q": "22px" }
        q = """<div class="q"><ul> %(q)s </ul></div>""" % {
            "q": "\n".join([ self.formatQuestion(x) for x in questions ])
        }
        t = """<div class="title">%(title)s</div>""" % {
            "title": self.formatTitle(self.title, self.subtitle)
        }
        # no title for back page
        if self.initialPos != 0:
            t = ""
        return """
        <style>
          .title  { font-size: %(sizes.title)s; }
          .q      { font-size: %(sizes.q)s; }
          .answer { color: red; }
        </style>
        %(title)s
        %(questions)s
        """ % {
            "sizes.title": sizes['title'],
            "sizes.q": sizes['q'],
            "title": t,
            "questions": q,
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

    def nextTextValid(self, label, text):
        doc = QtGui.QTextDocument(None)
        doc.setHtml(text)
        doc.setDefaultFont(label.font())
        doc.setTextWidth(800 - 55 - 135)
        size = doc.documentLayout().documentSize()
        log("size.height() > self.maxHeight: %d < %d" % (
            size.height(),
            self.maxHeight,
        ))
        if size.height() > self.maxHeight:
            return False
        label.setText(text)
        return True

    def finalize(self, label, pos):
        # log("pos: %d" % pos)
        hasNext = (pos < len(self.questions) - 1)
        # log("hasNext: %d" % hasNext)
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
            log("try: [%d:%d]" % (qIdx,qIdx+qCount))
            qSubset = self.questions[qIdx:qIdx+qCount]
            text = self.formatText(qSubset)
            if not self.nextTextValid(label, text):
                log("rejected")
                break
        return self.finalize(label, qIdx+qCount)

    def render(self):
        label = self.createLabel()
        text = self.formatText(self.questions)
        if self.initialPos != 0 or not self.nextTextValid(label, text):
            return self.chunkQ(label)
        log("one chunk !")
        return self.finalize(label, len(self.questions) - 1)


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "resources", "addition.yaml")
        with open(path) as f:
            self.additions = yaml.safe_load(f)
        QtWidgets.QMainWindow.__init__(self)
        self.qIndex = 0
        self.qPos = 0
        self.setFixedWidth(800)
        self.setFixedHeight(480)
        self.setQ(self.qIndex, self.qPos)

    def setBackgroundImage(self, name):
        path = os.path.join(os.path.dirname(__file__), "resources", name)
        # selpouvre: d4bee4
        # addition: ff9d82
        self.setStyleSheet("""
QMainWindow {
  border-image: url(\"%s\");
  background-color: #ff9d82;
}
QLabel {
  margin: 40px 55px 43px 135px;
}
""" % path);

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
        print("displaying question %d, backpage ? %d" % (self.qIndex+1, self.qPos != 0))
        renderer = AdditionRenderer(self.additions[self.qIndex], self.qPos)
        self.label, hasNext, nextPos = renderer.render()
        if hasNext:
            # self.setBackgroundImage("addition-back-arrow.png")
            self.setBackgroundImage("addition-back-arrow.png")
            self.nextIndex = self.qIndex
            self.nextPos = nextPos
        else:
            # self.setBackgroundImage("addition-back.png")
            self.setBackgroundImage("addition-back.png")
            if (self.qIndex + 1) != len(self.additions):
                self.nextIndex = self.qIndex + 1
                self.nextPos = 0

        self.pageNum = QLabel(self.label)
        self.pageNum.setText("<b>%s</b>" % (self.qIndex+1))
        self.pageNum.setMinimumHeight(110)
        self.pageNum.setMinimumWidth(75)
        self.pageNum.move(630, 400)
        self.pageNum.setStyleSheet("QLabel { color: #d4bee4 }")
        self.label.setParent(self)
        self.setCentralWidget(self.label)


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
