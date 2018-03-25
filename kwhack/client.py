# -*- coding: utf-8 -*-
"""
client

Created on 2018-03-19 by hbldh <henrik.blidh@nedomkull.com>

"""
import os
import time
import logging
import asyncio
from urllib.parse import urlsplit

import zmq

from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


def run_client(mongodb_uri, port):
    client = AsyncIOMotorClient(mongodb_uri)
    db_name = urlsplit(mongodb_uri).path.strip('/')
    collection = client[db_name]['blips']
    loop = asyncio.get_event_loop()

    async def store_blink(t):
        result = await collection.insert_one({'t': time.time(), 'v': float(t)})
        logger.debug('Inserted %s' % repr(result.inserted_id))

    #  Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    logger.debug("Collecting updates from LDR server...")
    socket.connect("tcp://localhost:%d" % port)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    while True:
        s = socket.recv_string()
        logger.debug("Received %r" % s)
        loop.run_until_complete(store_blink(s))


if __name__ == '__main__':
    import sys

    h = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S'
    )
    h.setFormatter(formatter)
    logger.addHandler(h)
    run_client(os.environ.get('MONGODB_URI'), port=5556)
