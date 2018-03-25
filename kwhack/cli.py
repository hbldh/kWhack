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

from kwhack import server
from kwhack import client


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
                str(pathlib.Path(str(args.output)).absolute()),
                encoding='utf-8'
            )
        h.setLevel(logging.DEBUG)
        client.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S'
        )
        h.setFormatter(formatter)
        client.logger.addHandler(h)
    client.run_client(os.environ.get('MONGODB_URI'), args.port)


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
                str(pathlib.Path(str(args.output)).absolute()),
                encoding='utf-8'
            )
        h.setLevel(logging.DEBUG)
        server.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S'
        )
        h.setFormatter(formatter)
        server.logger.addHandler(h)
    server.run_server(args.port)
