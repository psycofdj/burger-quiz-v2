#!/usr/bin/env python3
from PySide6 import QtCore

import datetime
import vlc
#import random
import wiringpi as wpi
import os.path
import time
import signal
import threading

from .lcd import LCD
from .btn import Btn
from .relay import Relay
from .led import LED

class App(QtCore.QObject):
    test = QtCore.Signal()
    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        wpi.wiringPiSetup()
        self.objs = []
        self.registerBtn("mayoPlusBtn",     26)
        self.registerBtn("mayoMinusBtn",    27)
        self.registerBtn("resetBtn",        24)
        self.registerBtn("ketchupPlusBtn",  23)
        self.registerBtn("ketchupMinusBtn", 22)
        self.registerBtn("nuggetsBtn",      21)
        self.registerBtn("selpoivreBtn",    14)
        self.registerBtn("menuBtn",         12)
        self.registerBtn("additionBtn",     13)
        self.registerBtn("sample1Btn",      3)
        self.registerBtn("sample2Btn",      7)
        self.registerBtn("sample3Btn",      0)
        self.registerBtn("sample4Btn",      2)
        self.registerBtn("ketchupBuzz", 10)
        self.registerBtn("mayoBuzz",    11)
        self.registerLED("ketchup", 5)
        self.registerLED("mayo", 6)
        self.registerRelay("relayMayo", 4)
        self.registerRelay("relayKetchup", 1)

        # self.set_scores(mayo=0, ketchup=0)
        # self.vlc = vlc.Instance("--no-xlib")
        # self.buzzer_player = self.vlc.media_player_new()
        # self.buzzer_player.audio_set_volume(100)
        # self.sample_player = self.vlc.media_player_new()
        # self.sample_player.audio_set_volume(100)
        self.last_buzzer = None
        self.is_playing = None
        self.stopped = False

    def registerLED(self, name, port):
        led = LED(port)
        self.objs.append(led)
        setattr(self, name, led)

    def registerRelay(self, name, port):
        relay = Relay(port)
        self.objs.append(relay)
        setattr(self, name, relay)

    def registerBtn(self, name, port, **kwds):
        btn = Btn(port, kind=Btn.NC, parent=self, **kwds)
        # def on_press():
        #     print("[btn:%s:%d] on_press" % (name, port))
        #     fn = getattr(self, "%s_on_press" % name, lambda: None)
        #     fn();
        # def on_release():
        #     print("[btn:%s:%d] on_release" % (name, port))
        #     fn = getattr(self, "%s_on_release" % name, lambda: None)
        #     fn();
        # def on_long_press():
        #     print("[btn:%s:%d] on_long_press" % (name, port))
        #     fn = getattr(self, "%s_on_long_press" % name, lambda: None)
        #     fn();
        # setattr(btn, "on_press", on_press)
        # setattr(btn, "on_release", on_release)
        # setattr(btn, "on_long_press", on_long_press)
        self.objs.append(btn)
        setattr(self, name, btn)

    def registerLCD(self, name, port):
        lcd = LCD(port)
        self.objs.append(lcd)
        setattr(self, name, lcd)

    # def ketchupPlus_on_press(self):
    #     self.ketchup.on()
    #     # self.add_scores(ketchup=1)
    # def ketchupMinus_on_press(self):
    #     self.ketchup.on()
    #     # self.add_scores(ketchup=-1)
    # def mayoPlus_on_press(self):
    #     self.mayo.on()
    #     # self.add_scores(mayo=1)
    # def mayoMinus_on_press(self):
    #     self.mayo.on()
    #     # self.add_scores(mayo=-1)
    # def ketchupPlus_on_release(self):
    #     self.ketchup.off()
    # def ketchupMinus_on_release(self):
    #     self.ketchup.off()
    # def mayoPlus_on_release(self):
    #     self.mayo.off()
    # def mayoMinus_on_release(self):
    #     self.mayo.off()

    # def random_tos(self):
    #     idx = random.randrange(0, len(self.tos), 1)
    #     #self.sc0.set_text(self.tos[idx])

    # def reset_on_press(self):
    #     self.test.emit()
    #     pass
    #     #self.random_tos()

    # def reset_on_long_press(self):
    #     self.mayo.blink(seconds=2, freq=35)
    #     self.ketchup.blink(seconds=2, freq=35)
    #     # self.set_scores(mayo=0, ketchup=0)

    def buzzlock(fn):
        def wrapper(self, *args, **kwargs):
            if self.last_buzzer is None:
                self.start_lock()
                fn(self, *args, **kwargs)
        return wrapper

    def start_lock(self):
        self.last_buzzer = datetime.datetime.now()

    def stop_lock(self):
        self.last_buzzer = None
        self.relayKetchup.off()
        self.relayMayo.off()

    def update_lock(self):
        if self.last_buzzer is None:
            return
        delay = datetime.timedelta(seconds=2)
        delta = datetime.datetime.now() - self.last_buzzer
        if delta >= delay:
            self.stop_lock()

    @buzzlock
    def ketchupBuzz_on_press(self):
        self.relayKetchup.on()
        self.ketchup.blink(seconds=2)
        # self.async_play("buzz-ketchup.mp3", player="buzzer_player")
    @buzzlock
    def mayoBuzz_on_press(self):
        self.relayMayo.on()
        self.mayo.blink(seconds=2)
        # self.async_play("buzz-mayo.mp3", player="buzzer_player")

    # def nuggets_on_press(self):
    #     pass
    #     #self.async_play("nuggets.mp3")
    # def selpoivre_on_press(self):
    #     pass
    #     #self.async_play("sel-ou-poivre.mp3")
    # def menu_on_press(self):
    #     pass
    #     #self.async_play("menus.mp3")
    # def addition_on_press(self):
    #     pass
    #     #self.async_play("addition.mp3")

    # def print_scores(self):
    #     pass
    #     # self.sc1.set_line(0, "== SCORES ==".center(20))
    #     # self.sc1.set_line(1, "ketchup".center(10) + "mayo".center(10))
    #     # self.sc1.set_line(2, str(self.scores["ketchup"]).center(10) + str(self.scores["mayo"]).center(10))

    # def add_scores(self, mayo=0, ketchup=0):
    #     self.set_scores(mayo=self.scores["mayo"]+mayo, ketchup=self.scores["ketchup"]+ketchup)

    # def set_scores(self, mayo, ketchup):
    #     self.scores = {
    #         "ketchup": ketchup,
    #         "mayo" : mayo,
    #     }
    #     self.print_scores()

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
        self.update_lock()
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
        # signal.signal(signal.SIGTERM, self.shutdown)
        #self.random_tos()
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
