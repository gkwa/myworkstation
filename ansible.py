from dataclasses import dataclass

import jinja2

from packages import PackageStore

TPL_STR1 = """{#- jinja2 -#}
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
{%- if casks %}
  - name: Install casks
    homebrew_cask:
      name: caskroom/versions/java8,{% for cask in casks %}{{ cask }}{{ "," if not loop.last }}{%- endfor %}
      state: present
{%- endif -%}
{% if brews %}
  - name: Install brews
    homebrew:
      name: {% for brew in brews %}{{ brew }}{{ "," if not loop.last }}{%- endfor %}
      state: present
{%- endif %}
"""

TPL_STR2 = """{#- jinja2 -#}
{%- set NEWLINE='\n' -%}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.
---

{% if mas -%}
# FIXME: mas is dictionary
{% for m in mas %}
#- name: Install mas {{m}}
#  homebrew_mas:
#    name: {{m}}
{%- endfor %}
{%- endif %}

{% if taps %}
{% for tap in taps %}
- name: Install tap {{tap}}
  homebrew_tap:
    name: {{tap}}
{%- endfor %}
{% endif %}

{% if casks %}
{% for cask in casks %}
- name: Install cask {{cask}}
  homebrew_cask:
    name: {{cask}}
{%- endfor %}
{% endif %}

{% if brews %}
{% for brew in brews %}
- name: Install brew {{brew}}
  homebrew:
    name: {{brew}}
{%- endfor %}
{% endif %}
"""


@dataclass
class Ansible:
    """Class to write out brew ansible format"""
    store: PackageStore
    config_basename: str = None
    template: jinja2.Template = None

    def __post_init__(self):
        self.config_basename = "macos{}.yml"
        self.template = jinja2.Template(TPL_STR1)

    def write_single_file(self):
        self.store.write_single_file(self.config_basename, self.template)

    def write_split_files(self):
        self.store.write_split_files(self.config_basename, self.template)

    def write_all_files(self):
        self.write_single_file()
        self.write_split_files()


def main():
    ps = PackageStore()
    ans = Ansible(ps)
    ans.write_all_files()


if __name__ == "__main__":
    main()
