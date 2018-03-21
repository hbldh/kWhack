# -*- coding: utf-8 -*-
"""
server

Created on 2018-03-19 by hbldh <henrik.blidh@nedomkull.com>

"""
import time
import logging

import zmq

from kwhack.ldr.ldrclass import LDRMeasurer

logger = logging.getLogger(__name__)


class LDRActivationDetector(object):

    def __init__(self):
        self.values = []
        self._is_active = False
        self._activation_time = None

    def __call__(self, value):
        self.values.append(int(value))
        if self.values[-1] < 1000:
            self._activation_time = time.time()
            self._is_active = True
        else:
            if self._is_active:
                self._is_active = False
                self.values = self.values[-1:]
                t = self._activation_time
                self._activation_time = None
                return t


def run_server(port):
    ldr = LDRMeasurer(7)
    detector = LDRActivationDetector()
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%d" % port)
    while True:
        t = ldr.rc_time()
        activation_t = detector(t)
        if activation_t:
            logger.debug('Send: %r' % t)
            socket.send_string(str(activation_t))


if __name__ == '__main__':
    import sys

    h = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S'
    )
    h.setFormatter(formatter)
    logger.addHandler(h)
    run_server(5556)
