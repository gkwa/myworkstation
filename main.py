#!/usr/bin/env python

import argparse
import logging

import packages

parser = argparse.ArgumentParser()

parser.add_argument(
    "--debug",
    action='store_true',
    default=False,
    help="debug")

args = parser.parse_args()

logging.basicConfig(format="%(asctime)s: %(message)s",
                    level=logging.DEBUG, datefmt="%H:%M:%S")


def main():
    ps = packages.PackageStore()
    ps.write_split_files(packages.ansible)
