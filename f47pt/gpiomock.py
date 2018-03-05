import random

class _GPIOMockClass(object):

    def __init__(self):
        self.mode = 1#GPIO.BOARD
        self.cfg = None
        self.pin_status = 0

        self.BOARD = 1

        self.LOW = 0
        self.HIGH = 1

        self.IN = 1
        self.OUT = 0

        self.PUD_DOWN = 0
        self.PUD_UP = 1

    def input(self, pin):
        return int(random.random() < 0.01)

    def setmode(self, mode):
        self.mode = mode

    def setup(self, pin, cfg, **kwargs):
        self.cfg = cfg

    def output(self, pin, status):
        pass

    def cleanup(self):
        pass


GPIO = _GPIOMockClass()
