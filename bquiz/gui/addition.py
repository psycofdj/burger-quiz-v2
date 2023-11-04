from bquiz.gui.question import QuestionFrame

class AdditionFrame(QuestionFrame):
    def __init__(self, handler, widget = None):
        super().__init__("addition-back.png", "addition-back-arrow.png", "#ff9d82", handler, widget)
