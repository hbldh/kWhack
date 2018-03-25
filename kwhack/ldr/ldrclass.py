# -*- coding: utf-8 -*-
"""
ldrclass

Created on 2018-03-05 by hbldh <henrik.blidh@nedomkull.com>

"""

import time
import logging

logger = logging.getLogger(__name__)
try:
    from RPi import GPIO
except:
    from kwhack.ldr.gpiomock import GPIO


class LDRMeasurer(object):

    def __init__(self, pin, t_setup=0.025, t_iteration=0.01):
        self.pin = pin
        self.t_setup = t_setup
        self.t_iteration = t_iteration

    def __enter__(self):
        logger.debug("LDRMeasurer: Running enter")
        GPIO.setmode(GPIO.BOARD)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("LDRMeasurer: Running exit")
        GPIO.cleanup()

    def _setup(self):
        GPIO.setmode(GPIO.BOARD)
        # Output on the pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.025)
        # Change the pin back to input
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def rc_time(self):
        self._setup()
        # Count until the pin goes high
        count = 0
        while GPIO.input(self.pin) == GPIO.LOW:
            count += 1
        return count

    def rc_time_with_sleep(self):
        self._setup()
        # Count until the pin goes high
        t = time.time()
        while GPIO.input(self.pin) == GPIO.LOW:
            time.sleep(self.t_iteration)
        return time.time() - t

    def rc_time_edge(self):
        self._setup()
        t = time.time()
        edge = GPIO.wait_for_edge(
            self.pin, GPIO.RISING, timeout=int(self.t_iteration * 1000)
        )
        return edge, time.time() - t


if __name__ == '__main__':
    with LDRMeasurer(7) as ldr:
        while True:
            print(ldr.rc_time())
