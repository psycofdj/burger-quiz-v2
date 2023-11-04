from bquiz.gui.question import QuestionFrame

class NuggetsFrame(QuestionFrame):
    def __init__(self, handler, widget = None):
        super().__init__("nuggets-back.png", "nuggets-back.png", "#ffff8d", handler, widget)

    def renderStyles(self, sizes):
        return """
         <style>
          .title      { font-size: %(title)s; font-weight: 600; }
          .question   { font-size: %(question)s; }
          .answer     { color: red; }
         </style>
        """ % sizes

    def renderChoice(self, value, isAnswer):
        itemClass = ""
        if isAnswer:
            itemClass = "answer"
        return """
          <li class="question %(class)s">%(value)s</li>
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
          <span class="title">%(idx)s. %(Q)s</span>
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
        questionsStr = [ self.renderQuestion(val, idx) for idx,val in enumerate(questions) ]
        return """
        <div>
        %s
        </div>""" % "<br/>".join(questionsStr)

    def hasPageBreak(self, questions):
        return True, questions[0:2], questions[2:]
