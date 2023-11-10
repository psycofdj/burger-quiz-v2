from PySide6 import QtCore
import wiringpi as wpi
import datetime

class Btn(QtCore.QObject):
    pressed = QtCore.Signal()
    longPressed = QtCore.Signal()
    released = QtCore.Signal()
    NO = 0
    NC = 1
    PRESSED = 1
    RELEASED = 0
    def __init__(self, name, port, parent=None, kind=NO, sensitivity=30):
        super().__init__(parent)
        wpi.pinMode(port, wpi.INPUT)
        wpi.pullUpDnControl(port, wpi.PUD_UP)
        self.setObjectName(name)
        self.sensitivity = sensitivity
        self.port = port
        self.kind = kind
        self.state = Btn.RELEASED
        self.events = 0
        self.pressed_since = None
        self.released_since = None

    def switch(self):
        self.events = 0
        if self.state == Btn.PRESSED:
            self.state = Btn.RELEASED
            self.pressed_since = None
            self.released_since = datetime.datetime.now()
            print("%s::released (port=%d)" % (self.objectName(), self.port))
            self.released.emit()
        else:
            self.pressed_since = datetime.datetime.now()
            self.state = Btn.PRESSED
            self.pressed.emit()
            print("%s::pressed (port=%d)" % (self.objectName(), self.port))

    def update(self):
        if self.released_since is not None:
            if datetime.datetime.now() - self.released_since > datetime.timedelta(seconds=0.15):
                self.released_since = None
            return
        state = wpi.digitalRead(self.port)
        if state == wpi.LOW and self.state == Btn.RELEASED:
            self.events += 1
        if state == wpi.HIGH and self.state == Btn.PRESSED:
            self.events += 1
        if self.events >= self.sensitivity:
            self.switch()
        if self.pressed_since is not None:
            if datetime.datetime.now() - self.pressed_since > datetime.timedelta(seconds=1):
                self.pressed_since = None
                self.longPressed.emit()
                print("%s::longPressed" % self.objectName())

    def finalize(self):
        pass
