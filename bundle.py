from itertools import zip_longest

import jinja2

import common

MAX_PACKAGES_PER_GROUP = 60

tpl_brewfile = jinja2.Template('''{#- jinja2 -#}
{% set NEWLINE='\n' -%}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.

{% if tap -%}
# taps
{% for t in tap -%}
tap "{{ t }}"
{% endfor %}
{%- endif -%}

{{NEWLINE}}

{%- if cask -%}
# cask
{% for c in cask -%}
cask "{{ c }}"
{% endfor %}
{%- endif -%}

{{NEWLINE}}

{%- if brew -%}
# brews
{% for b in brew -%}
brew "{{ b }}"
{% endfor %}
{%- endif -%}

{{NEWLINE}}

{%- if mas -%}
# mas
# FIXME: this is dictionary
{% for m in mas -%}
# mas "{{ m }}"
{% endfor %}
{%- endif -%}
''')


def write_single_file(packages):
    rtpl = tpl_brewfile.render({
        'tap': packages['tap'],
        'cask': packages['cask'],
        'brew': packages['brew'],
        'mas': packages['mas']}
    )
    with open('Brewfile', 'w') as brewfile:
        brewfile.write(rtpl)


def write_split_files(packages):
    brews = list(common.chunks(packages['brew'], MAX_PACKAGES_PER_GROUP // 2))
    cask = list(common.chunks(packages['cask'], MAX_PACKAGES_PER_GROUP // 2))
    # FIXME: add mas

    combined = list(zip_longest(brews, cask))

    for idx, lst in enumerate(combined):
        with open(f'Brewfile{idx+1}', 'w') as macos:
            dct = {
                'brew': combined[idx][0],
                'cask': combined[idx][1],
                'tap': packages['tap'],
                'mas': packages['mas']}
            tplr = tpl_brewfile.render(dct)
            macos.write(tplr)


def create_brewfiles(packages):
    write_single_file(packages)
    write_split_files(packages)
