#!/usr/bin/env python

import argparse
import logging
import sys

import ansible
import bundle
import common

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

parser = argparse.ArgumentParser()

parser.add_argument(
    "--debug",
    action='store_true',
    default=False,
    help="debug")

args = parser.parse_args()

logging.basicConfig(format="%(asctime)s: %(message)s",
                    level=logging.DEBUG, datefmt="%H:%M:%S")

packages = common.load('list.yml')
ansible.create_taskfiles(packages)
bundle.create_brewfiles(packages)
