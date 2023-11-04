from PySide6 import QtCore
import datetime
import wiringpi as wpi

class LED(QtCore.QObject):
    OFF = 0
    ON = 1
    FREQ = 25
    def __init__(self, name, port, parent=None):
        super().__init__(parent)
        wpi.pinMode(port, wpi.OUTPUT)
        self.setObjectName(name)
        self.port = port
        self.off()
        self.state = LED.OFF
        self.stop = None
        self.target = None
        self.freq = None

    def finalize(self):
        self.off()

    def update(self):
        if self.stop is None:
            return
        delta = self.stop - datetime.datetime.now()
        deltaMs = delta / datetime.timedelta(milliseconds=1)
        if deltaMs <= 0:
            if self.target == LED.OFF:
                self.off()
            else:
                self.on()
            self.target = None
            self.stop = None
            self.freq = None
        else:
            if int(deltaMs / 1000 * self.freq) % 2 == 0:
                self.on()
            else:
                self.off()

    @QtCore.Slot()
    def on(self):
        self.state = LED.ON
        wpi.digitalWrite(self.port, wpi.HIGH)

    @QtCore.Slot()
    def off(self):
        self.state = LED.OFF
        wpi.digitalWrite(self.port, wpi.LOW)

    @QtCore.Slot()
    def blink(self, seconds=5, freq=25, target=OFF):
        self.stop =  datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        self.freq = freq
        self.target = target
