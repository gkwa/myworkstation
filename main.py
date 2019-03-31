#!/usr/bin/env python

import argparse
import logging

import ansible
import bundle
import ci
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


ps = packages.PackageStore()
ans = ansible.Ansible(store=ps)
ans.write_all_files()
bdl = bundle.Bundle(store=ps)
bdl.write_all_files()
ci.write_all_files(ps, bdl, ans)
