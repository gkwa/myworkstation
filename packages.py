import os
import tempfile
from collections import namedtuple
from dataclasses import dataclass
from itertools import zip_longest
from typing import List

import jinja2

try:
    from yaml import CLoader as Loader, load, dump
except ImportError:
    from yaml import Loader, load, dump

MAX_PACKAGES_PER_GROUP = 10

Cm = namedtuple('Cm', 'basename template')

ansible = Cm('playbook{}.yml', jinja2.Template("""{#- jinja2 -#}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.
---
- hosts: localhost
  connection: local
  gather_facts: no
  tasks:
{% if mas -%}
# FIXME: dictionary
#   - name: Install mas's
#     homebrew_mas:
#       name: {% for m in mas %}{{ m }}{{ "," if not loop.last }}{%- endfor %}
{%- endif %}
{%- if taps %}
  - name: Install tap(s)
    homebrew_tap:
      name: {% for tap in taps %}{{ tap }}{{ "," if not loop.last }}{%- endfor %}
      state: present
{%- endif %}
  - name: Install java8 cask
    homebrew_cask:
      name: caskroom/versions/java8
      state: present
{%- if casks %}
  - name: Install casks
    homebrew_cask:
      name: {% for cask in casks %}{{ cask }}{{ "," if not loop.last }}{%- endfor %}
      state: present
{%- endif -%}
{% if brews %}
  - name: Install brews
    homebrew:
      name: {% for brew in brews %}{{ brew }}{{ "," if not loop.last }}{%- endfor %}
      state: present
{%- endif %}
"""))

bundle = Cm('Brewfile{}', jinja2.Template("""{#- Jinja2 -#}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.

{% if mas -%}
# FIXME: this is dictionary
{% for m in mas -%}
# mas "{{ m }}"
{% endfor -%}
{%- endif -%}

{% if taps -%}
{% for tap in taps -%}
tap "{{ tap }}"
{% endfor %}
{%- endif -%}

{%- if casks -%}
{% for cask in casks -%}
cask "{{ cask }}"
{% endfor %}
{%- endif -%}

{%- if brews -%}
{% for brew in brews -%}
brew "{{ brew }}"
{% endfor %}
{%- endif -%}
"""))


@dataclass
class PackageStore:
    """Class for keeping track of hombrew brews, casks, mas, etc."""
    brews: List[str] = None
    casks: List[str] = None
    taps: List[str] = None
    mas: List[str] = None
    fields: List[str] = None
    data_fname: str = None
    pairs: List = None

    def __post_init__(self):
        self.data_fname = 'list.yml'
        self.fields = ['brews', 'casks', 'taps', 'mas']
        dct = load(open(self.data_fname), Loader=Loader)
        for field in self.fields:
            setattr(self, field, dct[field])
        self.pairs = self.create_pairs()
        self.clean_yaml()

    def clean_yaml(self):
        fd, path = tempfile.mkstemp()
        f = os.fdopen(fd, 'w')
        d = {}
        for pkgtype in self.fields:
            x = getattr(self, pkgtype)
            try:
                y = set(x)  # FIXME: fails for mas which is dict
                z = sorted(y)
            except TypeError:
                z = x
            d[pkgtype] = z
        f.write(dump(d, default_flow_style=False))
        f.flush()
        os.rename(path, self.data_fname)

    def create_pairs(self):
        brews = list(chunks(self.brews, MAX_PACKAGES_PER_GROUP // 2))
        casks = list(chunks(self.casks, MAX_PACKAGES_PER_GROUP // 2))
        # FIXME: add mas

        return list(zip_longest(brews, casks))

    def get_map(self):
        d = {}
        for pkgtype in self.fields:
            d[pkgtype] = getattr(self, pkgtype)
        return d

    def split_targets(self, basename):
        d = []
        for idx, lst in enumerate(self.pairs):
            d.append(basename.format(idx + 1))

        return d

    def write_single_file(self, cm):
        target = cm.basename.format('')
        tmpl = cm.template
        with open(target, 'w') as fh:
            fh.write(tmpl.render(self.get_map()))

    def write_split_files(self, cm):
        d = self.split_targets(cm.basename)
        tmpl = cm.template
        for idx, lst in enumerate(self.pairs):
            target = d[idx]
            with open(target, 'w') as fh:
                dct = {
                    'brews': self.pairs[idx][0],
                    'casks': self.pairs[idx][1],
                    'taps': self.taps,
                    'mas': self.mas}
                fh.write(tmpl.render(dct))


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
