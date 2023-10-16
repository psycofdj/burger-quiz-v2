import datetime
import wiringpi as wpi

class LED:
    OFF = 0
    ON = 1
    FREQ = 25
    def __init__(self, port):
        wpi.pinMode(port, wpi.OUTPUT)
        self.port = port
        self.off()
        self.state = LED.OFF
        self.stop = None
        self.target = None
        self.freq = None

    def on(self):
        self.state = LED.ON
        wpi.digitalWrite(self.port, wpi.HIGH)

    def off(self):
        self.state = LED.OFF
        wpi.digitalWrite(self.port, wpi.LOW)

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

    def blink(self, seconds=5, freq=25, target=OFF):
        self.stop =  datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        self.freq = freq
        self.target = target
