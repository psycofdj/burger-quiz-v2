import wiringpi as wpi

class Relay:
    OFF = 0
    ON = 1
    def __init__(self, port):
        wpi.pinMode(port, wpi.OUTPUT)
        self.port = port
        self.off()

    def on(self):
        self.state = Relay.ON
        wpi.digitalWrite(self.port, wpi.HIGH)

    def off(self):
        self.state = Relay.OFF
        wpi.digitalWrite(self.port, wpi.LOW)

    def finalize(self):
        self.off()

    def update(self):
        pass
