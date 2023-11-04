from PySide6 import QtWidgets, QtGui, QtCore

from bquiz.gui.base import BaseFrame

class QuestionFrame(BaseFrame):
    def __init__(self, bg, altBg, bgColor, handler, widget):
        super().__init__(bg, altBg, bgColor, handler, widget)
        self.label = self.createLabel()

    def createLabel(self):
        font = QtGui.QFont("Ubuntu")
        font.setStretch(QtGui.QFont.ExtraCondensed)
        label = QtWidgets.QLabel(self)
        label.setFont(font)
        label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        label.setGeometry(120, 40, 800-180, 480-80)
        return label

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
        <div class="question">
          <ul>
          %s
          </ul>
        </div>
        """ % "\n".join([ self.renderQuestion(x) for x in questions ])

    def renderStyles(self, sizes = None):
        if not sizes:
            sizes = { "title": "28px", "question": "25px" }
        return """
        <style>
          .title    { font-size: %(title)s; }
          .question { font-size: %(question)s; }
          .answer   { color: red; }
        </style>
        """ % {
            "title": sizes['title'],
            "question": sizes['question'],
        }

    def renderChunk(self, chunk, sizes = None):
        styles = self.renderStyles(sizes)
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

    def fitsInLabel(self, text):
        height = self.getTextHeight(text)
        if height > self.label.height():
            return False
        return True

    def getTextHeight(self, text):
        doc = QtGui.QTextDocument(None)
        doc.setHtml(text)
        doc.setDefaultFont(self.label.font())
        doc.setTextWidth(self.label.width())
        return doc.documentLayout().documentSize().height()

    def hasPageBreak(self, questions):
        for cIdx,cQuestion in enumerate(questions):
            if cQuestion == "page-break":
                return True, questions[0:cIdx], questions[cIdx+1:]
        return False, [], []

    def render(self):
        hasPB, chunk1, chunk2 = self.hasPageBreak(self.questions)
        target = self.questions
        if hasPB:
            target = chunk1
            if self.initialPos != 0:
                target = chunk2
        for cSize in range(30, 15, -1):
            text = self.renderChunk(target, {
                "title": "%spx" % cSize,
                "question": "%spx" % (cSize - 2),
            })
            if self.fitsInLabel(text):
                self.label.setText(text)
                break
        hasNext = (hasPB and self.initialPos == 0)
        pos = len(target)
        return hasNext, pos

    def setItem(self, idx, item, initialPos):
        self.initialPos = initialPos
        self.title = item.get("title", "")
        self.subtitle = item.get("subtitle", None)
        self.questions = item.get("questions", [])
        return self.render()

    def mousePressEvent(self, event):
        if event.pos().x() > self.width() / 2:
            self.handler.nextQ()
        else:
            self.handler.prevQ()
