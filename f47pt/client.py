# -*- coding: utf-8 -*-
"""
client

Created on 2018-03-16 by hbldh <henrik.blidh@nedomkull.com>

"""

import logging
import asyncio
import socket

from f47pt.ldr.ldrclass import LDRMeasurer

logger = logging.getLogger(__name__)


def run_client(port=8888):
    loop = asyncio.get_event_loop()
    ldr = LDRMeasurer(7)

    async def send_ldr_measurement(message):
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', port, flags=socket.SO_REUSEADDR, loop=loop)
        logger.debug('Send: %r' % message)
        writer.write(message.encode())
        writer.close()

    try:
        while True:
            t = ldr.rc_time()
            loop.run_until_complete(send_ldr_measurement(str(t)))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if __name__ == '__main__':
    import sys
    h = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s: %(message)s',
                                  datefmt='%Y-%m-%dT%H:%M:%S')
    h.setFormatter(formatter)
    logger.addHandler(h)
    run_client()
