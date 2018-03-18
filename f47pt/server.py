# -*- coding: utf-8 -*-
"""
server

Created on 2018-03-16 by hbldh <henrik.blidh@nedomkull.com>

"""
import os
import time
import logging
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


def run_server(mongodb_uri, port=8888):
    client = AsyncIOMotorClient(mongodb_uri)
    collection = client['test']['mycoll']

    async def handle_connection(reader, writer):
        while True:
            data = await reader.read(100)
            message = data.decode()
            addr = writer.get_extra_info('peername')
            doc = {'t': time.time(), 'v': message}
            logger.debug("Received %r from %r" % (
                str(message), addr))
            result = await collection.insert_one(doc)
            logger.debug("Inserted: %r as %r" % (
                str(doc), str(result.inserted_id)))
        writer.close()

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(
        handle_connection, '127.0.0.1', port, loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    logger.info('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    import sys
    h = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s: %(message)s',
                                  datefmt='%Y-%m-%dT%H:%M:%S')
    h.setFormatter(formatter)
    logger.addHandler(h)
    run_server(os.environ.get('MONGODB_URI'))






