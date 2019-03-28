#!/usr/bin/env python

import argparse
import logging
import sys
from itertools import zip_longest

import sys
import pprint
import jinja2
import toml

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

MAX_PACKAGES_PER_GROUP = 60

dct = toml.load('list.toml')
pprint.pprint(dct)

sys.exit(0)

dct['brews'] = sorted(set(dct['brews']))
dct['taps'] = sorted(set(dct['taps']))
dct['casks'] = sorted(set(dct['casks']))
dct['mass'] = dct['mass']  # FIXME

with open('list.toml', 'w') as outfile:
    toml.dump(dct, outfile)


tpl_str = '''{#- jinja2 -#}
{% set NEWLINE='\n' -%}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.
---

{% if taps -%}
- homebrew_tap:
  name: {% for tap in taps %}{{ tap }}{{ ", " if not loop.last }}{%- endfor %}
{% endif -%}

{{NEWLINE}}

{%- if casks -%}
- homecask_cask:
  name: caskroom/versions/java8, {% for cask in casks %}{{ cask }}{{ ", " if not loop.last }}{%- endfor %}
{% endif -%}

{{NEWLINE}}

{%- if brews -%}
- homebrew:
  name: {% for brew in brews %}{{ brew }}{{ ", " if not loop.last }}{%- endfor %}
  upgrade_all: yes
{% endif -%}
'''

with open(f'macos.toml', 'w') as macos:
    dct = {'brews': dct['brews'], 'casks': dct['casks'], 'taps': dct['taps']}
    tplr = jinja2.Template(tpl_str).render(dct)
    macos.write(tplr)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


tpl = jinja2.Template(
    tpl_str,
    trim_blocks=True,
    keep_trailing_newline=False,
    lstrip_blocks=True,)

brews = list(chunks(dct['brews'], MAX_PACKAGES_PER_GROUP // 2))
casks = list(chunks(dct['casks'], MAX_PACKAGES_PER_GROUP // 2))
# FIXME: add mas

combined = list(zip_longest(brews, casks))

for idx, lst in enumerate(combined):
    with open(f'macos{idx+1}.toml', 'w') as macos:
        dct = {
            'brews': combined[idx][0],
            'casks': combined[idx][1],
            'taps': dct['taps'],}
        tplr = jinja2.Template(tpl_str).render(dct)
        macos.write(tplr)

Python finished at Thu Mar 28 12:55:34
