from PySide6 import QtCore
import wiringpi as wpi

class Relay(QtCore.QObject):
    OFF = 0
    ON = 1
    def __init__(self, name, port, parent = None):
        super().__init__(parent)
        wpi.pinMode(port, wpi.OUTPUT)
        self.setObjectName(name)
        self.port = port
        self.off()

    @QtCore.Slot()
    def on(self):
        self.state = Relay.ON
        wpi.digitalWrite(self.port, wpi.HIGH)

    @QtCore.Slot()
    def off(self):
        self.state = Relay.OFF
        wpi.digitalWrite(self.port, wpi.LOW)

    def finalize(self):
        self.off()

    def update(self):
        pass
