# -*- coding: utf-8 -*-
"""
server

Created on 2018-03-19 by hbldh <henrik.blidh@nedomkull.com>

"""
import logging

import zmq

from kwhack.ldr.ldrclass import LDRMeasurer

logger = logging.getLogger(__name__)


def run_server(port):
    ldr = LDRMeasurer(7)
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%d" % port)

    while True:
        t = ldr.rc_time()
        logger.debug('Send: %r' % t)
        socket.send_string()


if __name__ == '__main__':
    import sys
    h = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s: %(message)s',
                                  datefmt='%Y-%m-%dT%H:%M:%S')
    h.setFormatter(formatter)
    logger.addHandler(h)
    run_server(5556)
