import wiringpi as wpi
import datetime

class Btn:
    NO = 0
    NC = 1
    Pressed = 1
    Released = 0
    def __init__(self, port, kind=NO, sensitivity=30):
        wpi.pinMode(port, wpi.INPUT)
        wpi.pullUpDnControl(port, wpi.PUD_UP)
        self.sensitivity = sensitivity
        self.port = port
        self.kind = kind
        self.state = Btn.Released
        self.on_press = lambda *args: None
        self.on_release = lambda *args: None
        self.events = 0
        self.pressed_since = None
        self.released_since = None

    def fire(self, event):
        fn = getattr(self, event, None)
        if fn is not None:
            fn()

    def switch(self):
        self.events = 0
        if self.state == Btn.Pressed:
            self.state = Btn.Released
            self.pressed_since = None
            self.released_since = datetime.datetime.now()
            self.fire("on_release")
        else:
            self.pressed_since = datetime.datetime.now()
            self.state = Btn.Pressed
            self.fire("on_press")

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
                self.fire("on_long_press")

    def finalize(self):
        pass
