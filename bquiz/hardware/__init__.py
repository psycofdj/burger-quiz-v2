#!/usr/bin/env python3
from PySide6 import QtCore

import wiringpi as wpi
import signal
import threading

from .lcd import LCD
from .btn import Btn
from .relay import Relay
from .led import LED

class Hardware(QtCore.QObject):
    test = QtCore.Signal()
    def __init__(self, parent = None):
        super().__init__(parent)
        wpi.wiringPiSetup()
        self.stopped = False
        self.objs = []
        self.registerBtn("mayoPlusBtn",     22)
        self.registerBtn("mayoMinusBtn",    23)
        self.registerBtn("resetBtn",        26)
        self.registerBtn("ketchupPlusBtn",  24)
        self.registerBtn("ketchupMinusBtn", 27)
        self.registerBtn("nuggetsBtn",      2)
        self.registerBtn("selpoivreBtn",    0)
        self.registerBtn("menusBtn",        7)
        self.registerBtn("additionBtn",     3)
        self.registerBtn("sample1Btn",      21)
        self.registerBtn("sample2Btn",      14)
        self.registerBtn("sample3Btn",      13)
        self.registerBtn("sample4Btn",      12)
        self.registerBtn("ketchupBuzz",     10)
        self.registerBtn("mayoBuzz",        11)
        self.registerLED("ketchupLED",      5)
        self.registerLED("mayoLED",         6)
        self.registerRelay("mayoRelay",     1)
        self.registerRelay("ketchupRelay",  4)

    def registerLED(self, name, port):
        led = LED(name, port, self)
        self.objs.append(led)
        setattr(self, name, led)

    def registerRelay(self, name, port):
        relay = Relay(name, port, self)
        self.objs.append(relay)
        setattr(self, name, relay)

    def registerBtn(self, name, port, **kwds):
        btn = Btn(name, port, kind=Btn.NC, parent=self, **kwds)
        self.objs.append(btn)
        setattr(self, name, btn)

    def registerLCD(self, name, port):
        lcd = LCD(port)
        self.objs.append(lcd)
        setattr(self, name, lcd)

    def update(self):
        for c_obj in self.objs:
            c_obj.update()

    def finalize(self):
        for c_obj in self.objs:
            c_obj.finalize()

    def shutdown(self, signal, stackframe):
        print("burger quiz stop requested")
        self.stopped = True

    def run(self):
        print("burger quiz is running")
        try:
            while not self.stopped:
                self.update()
        except KeyboardInterrupt:
            pass

        self.finalize()
        print("burger quiz stopped")

    def spawn(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        return thread
