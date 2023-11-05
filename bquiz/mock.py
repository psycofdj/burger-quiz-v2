import sys
import time
import threading
from PySide6 import QtGui, QtCore, QtWidgets, QtGui

class MockBtn(QtWidgets.QPushButton):
    longPressed = QtCore.Signal()
    def __init__(self, name, parent = None):
        super().__init__(parent)
        self.setText(name)

class MockLED(QtWidgets.QWidget):
    def __init__(self, name, parent = None):
        super().__init__(parent)
    def on(self):
        pass
    def off(self):
        pass
    def blink(self, *args, **kwds):
        pass

class MockRelay(QtWidgets.QWidget):
    def __init__(self, name, parent = None):
        super().__init__(parent)
    def on(self):
        pass
    def off(self):
        pass

class Mock(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QWidget()
        self.mayoPlusBtn = MockBtn("mayoPlusBtn")
        self.mayoMinusBtn = MockBtn("mayoMinusBtn")
        self.resetBtn = MockBtn("resetBtn")
        self.ketchupPlusBtn = MockBtn("ketchupPlusBtn")
        self.ketchupMinusBtn = MockBtn("ketchupMinusBtn")
        self.nuggetsBtn = MockBtn("nuggetsBtn")
        self.selpoivreBtn = MockBtn("selpoivreBtn")
        self.menusBtn = MockBtn("menusBtn")
        self.additionBtn = MockBtn("additionBtn")
        self.mayoBuzz = MockBtn("mayoBuzz")
        self.ketchupBuzz = MockBtn("ketchupBuzz")
        self.sample1Btn = MockBtn("sample1Btn")
        self.sample2Btn = MockBtn("sample2Btn")
        self.sample3Btn = MockBtn("sample3Btn")
        self.sample4Btn = MockBtn("sample4Btn")
        self.ketchupLED = MockLED("ketchupLED")
        self.mayoLED = MockLED("ketchupLED")
        self.ketchupRelay = MockRelay("ketchupRelay")
        self.mayoRelay = MockRelay("ketchupRelay")
        self.bye = MockBtn("bye")
        self.box = QtWidgets.QVBoxLayout(self.widget)
        self.box.addWidget(self.mayoPlusBtn)
        self.box.addWidget(self.mayoMinusBtn)
        self.box.addWidget(self.resetBtn)
        self.box.addWidget(self.ketchupPlusBtn)
        self.box.addWidget(self.ketchupMinusBtn)
        self.box.addWidget(self.nuggetsBtn)
        self.box.addWidget(self.selpoivreBtn)
        self.box.addWidget(self.menusBtn)
        self.box.addWidget(self.additionBtn)
        self.box.addWidget(self.sample1Btn)
        self.box.addWidget(self.sample2Btn)
        self.box.addWidget(self.sample3Btn)
        self.box.addWidget(self.sample4Btn)
        self.box.addWidget(self.bye)
        self.box.addWidget(self.mayoBuzz)
        self.box.addWidget(self.ketchupBuzz)
        self.setCentralWidget(self.widget)
        self.bye.clicked.connect(self.doBye)

    @QtCore.Slot()
    def doBye(self):
        sys.exit(1)

    def run(self):
        pass

    def spawn(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        return thread
