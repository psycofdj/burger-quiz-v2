from PySide6 import QtCore
import wiringpi as wpi
import datetime

class Btn(QtCore.QObject):
    pressed = QtCore.Signal()
    longPressed = QtCore.Signal()
    released = QtCore.Signal()
    NO = 0
    NC = 1
    Pressed = 1
    Released = 0
    def __init__(self, port, parent=None, kind=NO, sensitivity=30):
        QtCore.QObject.__init__(self, parent)
        wpi.pinMode(port, wpi.INPUT)
        wpi.pullUpDnControl(port, wpi.PUD_UP)
        self.sensitivity = sensitivity
        self.port = port
        self.kind = kind
        self.state = Btn.Released
        self.events = 0
        self.pressed_since = None
        self.released_since = None

    def switch(self):
        self.events = 0
        if self.state == Btn.Pressed:
            self.state = Btn.Released
            self.pressed_since = None
            self.released_since = datetime.datetime.now()
            self.released.emit()
        else:
            self.pressed_since = datetime.datetime.now()
            self.state = Btn.Pressed
            self.pressed.emit()

    def update(self):
        if self.released_since is not None:
            if datetime.datetime.now() - self.released_since > datetime.timedelta(seconds=0.15):
                self.released_since = None
            return
        state = wpi.digitalRead(self.port)
        if state == wpi.LOW and self.state == Btn.Released:
            self.events += 1
        if state == wpi.HIGH and self.state == Btn.Pressed:
            self.events += 1
        if self.events >= self.sensitivity:
            self.switch()
        if self.pressed_since is not None:
            if datetime.datetime.now() - self.pressed_since > datetime.timedelta(seconds=1):
                self.pressed_since = None
                self.longPressed.emit()

    def finalize(self):
        pass
