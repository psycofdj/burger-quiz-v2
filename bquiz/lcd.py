import datetime
import math

from . import lcddriver

class LCD:
    class Caterpillar:
        LINEOFFSET = [0x80, 0xC0, 0x94, 0xD4]
        MASK = {
            "frame1": [
                "10010010010010010010",
                "0                  0",
                "0                  1",
                "10010010010010010010",
            ],
            "frame2": [
                "01001001001001001001",
                "0                  0",
                "1                  0",
                "00100100100100100101",
            ],
            "frame3": [
                "00100100100100100100",
                "1                  1",
                "0                  0",
                "01001001001001001010",
            ],
        }
        def __init__(self, delay_ms=150):
            self.delay_ms = delay_ms
            self.frame = "frame1"
            self.start_time = datetime.datetime.now()

        def display_frame(self, handler):
            handler.lcd_write(lcddriver.LCD_RETURNHOME)
            for c_idx, c_mask in enumerate(LCD.Caterpillar.MASK[self.frame]):
                offset = LCD.Caterpillar.LINEOFFSET[c_idx]
                for c_addr, c_char in enumerate(c_mask):
                    handler.lcd_write(offset + c_addr)
                    if c_char == "1":
                        handler.lcd_write(0b00101010, lcddriver.Rs)
                    elif c_char == "0":
                        handler.lcd_write(ord(" "), lcddriver.Rs)

        def next_frame(self):
            if self.frame == "frame1":
                self.frame = "frame2"
            elif self.frame == "frame2":
                self.frame = "frame3"
            elif self.frame == "frame3":
                self.frame = "frame1"
            self.start_time = self.start_time + datetime.timedelta(milliseconds=self.delay_ms)

        def update(self, handler):
            delta = datetime.datetime.now() - self.start_time
            deltaMs = delta / datetime.timedelta(milliseconds=1)
            if deltaMs > self.delay_ms:
                self.next_frame()
                self.display_frame(handler)

    class Line:
        LEFT = 0
        RIGHT = 1
        def __init__(self, text="", justify=LEFT, speed=3):
            self.cursor = 0
            self.text = text
            self.justify = justify
            self.speed = speed
            self.last = datetime.datetime.now()

        def draw(self, handler, idx):
            fmt = "%20s"
            if self.justify == LCD.Line.LEFT:
                fmt = "%- 20s"
            val = fmt % self.text[self.cursor-20:self.cursor]
            handler.lcd_display_string(val, idx + 1)
            self.last = datetime.datetime.now()

        def update(self, handler, idx):
            if self.cursor >= len(self.text):
                return
            if self.cursor == 0:
                self.cursor += 20
                self.draw(handler, idx)
            else:
                elapsed = datetime.datetime.now() - self.last
                elapsedMs = elapsed / datetime.timedelta(milliseconds=1)
                nb = math.floor(float(elapsedMs) * float(self.speed) / float(1000))
                if nb > 0:
                    self.cursor += nb
                    self.draw(handler, idx)

    def __init__(self, i2cPort):
        self.lines = [ LCD.Line(), LCD.Line(), LCD.Line(), LCD.Line() ]
        self.handler = lcddriver.lcd(i2cPort)
        self.bg_off()
        self.caterpillar = None


    def set_text(self, text):
        lines = [[]]
        words = text.split(" ")
        for word in words:
            w = len(word)
            l = len(" ".join(lines[-1]))
            if l + w < 20:
                lines[-1].append(word)
            else:
                lines.append([word])
        self.handler.lcd_clear()
        for idx, words in enumerate(lines):
            if idx > 3:
                break
            self.set_line(idx, " ".join(words))

    def set_line(self, idx, text="", justify=Line.LEFT, speed=3):
        self.bg_on()
        self.lines[idx] = LCD.Line(text, justify, speed)

    def bg_off(self):
        self.handler.lcd_backlight("off")

    def bg_on(self):
        self.handler.lcd_backlight("on")

    def add_caterpillar(self):
        self.caterpillar = LCD.Caterpillar()

    def update(self):
        for c_idx, c_line in enumerate(self.lines):
            c_line.update(self.handler, c_idx)
        if self.caterpillar is not None:
            self.caterpillar.update(self.handler)

    def finalize(self):
        self.bg_off()
