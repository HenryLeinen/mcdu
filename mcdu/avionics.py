import time

class Avionics(object):
    _instance = None

    def __new__(cls, *args):
        if not cls._instance:
            cls._instance = super(Avionics, cls).__new__(cls, *args)
            cls._instance.init()

        return cls._instance

    def init(self):
        self.active = False

        self.pos = (0.0, 0.0)
        self.speed = 0
        self.hdg = 0
        self.alt = 0
        self.wind = "0/0"
        self.temp = 0
        self.brk = True
        self.gear = True
        self.eng = (0.0, 0.0, 0.0, 0.0)

        self.reset()

    def reset(self):
        self.progress = 0
        self.hdg_change = 0
        self.alt_change = 0

    def update(self, data):
        if self.active:
            if "hdg" in data:
                self.hdg_change += abs(self.hdg - data["hdg"])

            if "alt" in data:
                self.alt_change += abs(self.alt - data["alt"])

            self.analyze()

        for key, value in data.items():
            setattr(self, key, value)

        self.active = True

    def analyze(self):
        # detect out
        if self.progress == 0:
            if not self.brk:
                self.progress += 1

        # detect off
        elif self.progress == 1:
            if not self.gear or self.alt_change > 200:
                self.progress += 1

        # detect on
        elif self.progress == 2:
            if self.gear and self.speed < 50:
                self.progress += 1

        # detect in
        elif self.progress == 3:
            if not self.speed and self.brk and self.eng < (5, 5, 5, 5):
                self.progress += 1
