# -*- coding: utf-8 -*-
"""
client

Created on 2018-03-16 by hbldh <henrik.blidh@nedomkull.com>

"""
import logging
import asyncio

from f47pt.ldr.ldrclass import LDRMeasurer

logger = logging.getLogger(__name__)


def run_client(port=8888):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run_client(port))


async def _run_client(port=8888, loop=None):
    loop = loop if loop else asyncio.get_event_loop()
    ldr = LDRMeasurer(7)
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', port, loop=loop)
    try:
        while True:
            t = ldr.rc_time()
            logger.debug('Send: %r' % t)
            writer.write(str(t).encode())
    except KeyboardInterrupt:
        pass
    finally:
        writer.close()


if __name__ == '__main__':
    run_client()
