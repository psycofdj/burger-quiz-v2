from bquiz.gui.question import QuestionFrame

class SelPoivreFrame(QuestionFrame):
    def __init__(self, handler, widget = None):
        super().__init__("selpoivre-back.png", "selpoivre-back-arrow.png", "#d4bee4", handler, widget)
