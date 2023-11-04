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
        self.registerBtn("mayoPlusBtn",     26)
        self.registerBtn("mayoMinusBtn",    27)
        self.registerBtn("resetBtn",        24)
        self.registerBtn("ketchupPlusBtn",  23)
        self.registerBtn("ketchupMinusBtn", 22)
        self.registerBtn("nuggetsBtn",      21)
        self.registerBtn("selpoivreBtn",    14)
        self.registerBtn("menusBtn",        12)
        self.registerBtn("additionBtn",     13)
        self.registerBtn("sample1Btn",      3)
        self.registerBtn("sample2Btn",      7)
        self.registerBtn("sample3Btn",      0)
        self.registerBtn("sample4Btn",      2)
        self.registerBtn("ketchupBuzz",     10)
        self.registerBtn("mayoBuzz",        11)
        self.registerLED("ketchupLED",      5)
        self.registerLED("mayoLED",         6)
        self.registerRelay("mayoRelay",     4)
        self.registerRelay("ketchupRelay",  1)
        # self.vlc = vlc.Instance("--no-xlib")
        # self.buzzer_player = self.vlc.media_player_new()
        # self.buzzer_player.audio_set_volume(100)
        # self.sample_player = self.vlc.media_player_new()
        # self.sample_player.audio_set_volume(100)

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

    # def async_play(self, name, player="sample_player"):
    #     path = os.path.join(
    #         os.path.dirname(__file__),
    #         "resources",
    #         name,
    #     )
    #     handler = getattr(self, player, self.sample_player)
    #     handler.set_media(self.vlc.media_new(path))
    #     print("[media:%s]: playing %s" % (player, name))
    #     handler.play()

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
