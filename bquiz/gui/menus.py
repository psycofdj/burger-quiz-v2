from bquiz.gui.question import QuestionFrame

class MenusFrame(QuestionFrame):
    def __init__(self, handler, widget = None):
        super().__init__("menus-back.png", "menus-back-arrow.png", "#cfffff", handler, widget)
    def setItem(self, idx, item, pos):
        if idx == 2:
            self.setColor("#ffd38f")
        else:
            self.setColor("#cfffff")
        return super().setItem(idx, item, pos)
