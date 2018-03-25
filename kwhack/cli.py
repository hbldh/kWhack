# -*- coding: utf-8 -*-
"""
cli

Created on 2018-03-18 by hbldh <henrik.blidh@nedomkull.com>

"""
import os
import sys
import argparse
import logging
import pathlib

from kwhack.server import run_server
from kwhack.client import run_client

logger = logging.getLogger(__name__)


def cli_client():
    parser = argparse.ArgumentParser(
        description='Power consumption tracker client'
    )
    parser.add_argument('-p', '--port', default=8888)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--output', type=str, default='-')
    args = parser.parse_args()
    if args.verbose:
        if args.output == '-':
            h = logging.StreamHandler(sys.stdout)
        else:
            h = logging.FileHandler(
                pathlib.Path(str(args.output).absolute()), encoding='utf-8'
            )
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S'
        )
        h.setFormatter(formatter)
        logger.addHandler(h)
    run_client(os.environ.get('MONGODB_URI'), args.port)


def cli_server():
    parser = argparse.ArgumentParser(
        description='Power consumption tracker server'
    )
    parser.add_argument('-p', '--port', default=8888)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--output', type=str, default='-')
    args = parser.parse_args()
    if args.verbose:
        if args.output == '-':
            h = logging.StreamHandler(sys.stdout)
        else:
            h = logging.FileHandler(
                pathlib.Path(str(args.output).absolute()), encoding='utf-8'
            )
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S'
        )
        h.setFormatter(formatter)
        logger.addHandler(h)
    run_server(args.port)
