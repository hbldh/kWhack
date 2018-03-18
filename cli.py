# -*- coding: utf-8 -*-
"""
cli

Created on 2018-03-18 by hbldh <henrik.blidh@nedomkull.com>

"""
import os
import sys
import argparse
import logging

from f47pt.server import run_server
from f47pt.client import run_client

logger = logging.getLogger(__name__)


def cli_server():
    parser = argparse.ArgumentParser(
        description='Power consumption tracker server')
    parser.add_argument('p', '--port', default=8888)
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        h = logging.StreamHandler(sys.stdout)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(name)s: %(message)s',
                                      datefmt='%Y-%m-%dT%H:%M:%S')
        h.setFormatter(formatter)
        logger.addHandler(h)

    run_server(os.environ.get('MONGODB_URI'), args.port)


def cli_client():
    parser = argparse.ArgumentParser(
        description='Power consumption tracker client')
    parser.add_argument('p', '--port', default=8888)
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        h = logging.StreamHandler(sys.stdout)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(name)s: %(message)s',
                                      datefmt='%Y-%m-%dT%H:%M:%S')
        h.setFormatter(formatter)
        logger.addHandler(h)

    run_client(args.port)


