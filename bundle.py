from dataclasses import dataclass

import jinja2

from packages import PackageStore

TPL_STR = """{#- Jinja2 -#}
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
"""


@dataclass
class Bundle:
    """Class to write out brew bundler format"""
    store: PackageStore
    config_basename: str = None
    template: jinja2.Template = None

    def __post_init__(self):
        self.config_basename = "Brewfile{}"
        self.template = jinja2.Template(TPL_STR)

    def write_single_file(self):
        self.store.write_single_file(
            self.config_basename, self.template)

    def write_split_files(self):
        self.store.write_split_files(
            self.config_basename, self.template)

    def write_all_files(self):
        self.write_single_file()
        self.write_split_files()


def main():
    ps = PackageStore()
    bdl = Bundle(ps)
    bdl.write_all_files()


if __name__ == "__main__":
    main()
